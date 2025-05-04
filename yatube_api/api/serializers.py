"""
Сериализаторы для моделей приложения API Yatube.

В этом модуле описаны сериализаторы для моделей Group, Post, Comment и Follow,
которые используются для преобразования данных между JSON и моделями Django.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from posts.models import Group, Post, Comment, Follow


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Мета-данные для GroupSerializer."""

        model = Group
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        """Мета-данные для PostSerializer."""

        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Мета-данные для CommentSerializer."""

        model = Comment
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        """Мета-данные для FollowSerializer."""

        model = Follow
        fields = ("user", "following")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following"),
                message="Подписка уже существует",
            ),
        ]

    def validate(self, data):
        """
        Проверяет, что пользователь не подписывается на самого себя.

        Выбрасывает ValidationError, если user == following.
        """
        if data["user"] == data["following"]:
            raise serializers.ValidationError("Нельзя подписаться на себя")
        return data
