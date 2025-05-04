from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, Follow

from api.serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer,
)
from api.permissions import IsObjectAuthorOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с группами.

    Предоставляет доступ только для чтения:
    - Получение списка групп.
    - Получение деталей группы.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с постами.

    Предоставляет доступ к полному набору операций с постами:
    - Получение списка постов.
    - Создание, обновление, удаление постов.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsObjectAuthorOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Сохраняет пост с автором, привязанным к текущему пользователю.
        """

        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями.

    Предоставляет доступ к операциям с комментариями:
    - Получение списка комментариев.
    - Создание, обновление, удаление комментариев.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsObjectAuthorOrReadOnly,
    )

    def perform_create(self, serializer):
        """
        Сохраняет комментарий, привязывая его к посту и текущему пользователю.
        """

        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        """
        Возвращает все комментарии для конкретного поста.
        """

        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post.comments.all()


class FollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet для работы с подписками.

    Позволяет создавать подписки на пользователей и просматривать список подписок.
    """

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def perform_create(self, serializer):
        """
        Создает подписку, привязывая ее к текущему пользователю.
        """

        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Возвращает все подписки текущего пользователя.
        """
        
        follows = Follow.objects.filter(user__exact=self.request.user)
        return follows
