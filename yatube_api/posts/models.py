from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator
from django.utils.html import format_html

User = get_user_model()


def get_truncated_span_from_text(text):
    """Return truncated text with tooltip for the admin panel."""

    truncated = Truncator(text).chars(64)
    span = '<span title="{}">{}</span>'
    return format_html(span, text, truncated)


class Group(models.Model):
    """Group model for Data Base.

    Columns:
        title - Char[128];
        slug - Slug, unique;
        description - Text.
    """

    title = models.CharField(verbose_name='Название', max_length=128)
    slug = models.SlugField(verbose_name='Slug', unique=True)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def short_description(self):
        return get_truncated_span_from_text(self.description)


class Post(models.Model):
    """Post model for Data Base.

    Columns:
        text - Text;
        author - FK(User), delete cascade, related name = 'posts';
        group - FK(Group), delete cascade, related name = 'posts', null, blank;
        image - Image, folder = 'posts/', null, blank;
        pub_date - DateTime, auto_now_add.
    """

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE, related_name='posts'
    )
    group = models.ForeignKey(
        Group, verbose_name='Группа',
        on_delete=models.CASCADE, related_name='posts',
        null=True, blank=True
    )
    image = models.ImageField(
        verbose_name='Фотография', upload_to='posts/',
        null=True, blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return Truncator(self.text).chars(64)

    def short_text(self):
        return get_truncated_span_from_text(self.text)


class Comment(models.Model):
    """Comment model for Data Base.

    Columns:
        text - Text;
        author - FK(User), delete cascade, related name = 'comments';
        post - FK(Post), delete cascade, related name = 'comments';
        created - DateTime, auto_now_add.
    """

    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, verbose_name='Пост',
        on_delete=models.CASCADE, related_name='comments'
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return Truncator(self.text).chars(60)

    def short_text(self):
        return get_truncated_span_from_text(self.text)


class Follow(models.Model):
    """Follow model for Data Base.

    Provides a system of user subscriptions to each other.
    The object is a couple of users (`user` is following `following`).
    Columns:
        follower - FK(User), delete cascade, related name = 'follower';
        following - FK(User), delete cascade, related name = 'following'.
    """

    user = models.ForeignKey(
        User, verbose_name='Подписчик',
        on_delete=models.CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        User, verbose_name='Подписан',
        on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            ),
        ]