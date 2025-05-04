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
    """
    Модель Group для базы данных.

    Представляет собой сообщество или группу постов.

    Поля:
        title — строковое поле (до 128 символов);
        slug — поле типа Slug, уникальное;
        description — текстовое поле.
    """

    title = models.CharField(verbose_name="Название", max_length=128)
    slug = models.SlugField(verbose_name="Slug", unique=True)
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ("title",)

    def __str__(self):
        return self.title

    def short_description(self):
        return get_truncated_span_from_text(self.description)


class Post(models.Model):
    """
    Модель Post для базы данных.

    Представляет собой публикацию пользователя.

    Поля:
        text — текстовое поле для содержимого поста;
        author — внешний ключ на модель User, каскадное удаление,
        related_name='posts';
        group — внешний ключ на модель Group, каскадное удаление,
        related_name='posts', может быть пустым (null, blank);
        image — поле для изображения, сохраняется в папку 'posts/',
        может быть пустым (null, blank);
        pub_date — дата и время публикации, автоматически устанавливается
        при создании записи.
    """

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE,
        related_name="posts"
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Группа",
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name="Фотография", upload_to="posts/", null=True,
        blank=True
    )
    pub_date = models.DateTimeField(verbose_name="Дата публикации",
                                    auto_now_add=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ("-pub_date",)

    def __str__(self):
        return Truncator(self.text).chars(64)

    def short_text(self):
        return get_truncated_span_from_text(self.text)


class Comment(models.Model):
    """
    Модель Comment для базы данных.

    Представляет собой комментарий к посту.

    Поля:
        text — текстовое поле для содержимого комментария;
        author — внешний ключ на модель User, каскадное удаление,
        related_name='comments';
        post — внешний ключ на модель Post, каскадное удаление,
        related_name='comments';
        created — дата и время создания комментария, автоматически
        устанавливается при создании записи.
    """

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        Post, verbose_name="Пост", on_delete=models.CASCADE,
        related_name="comments"
    )
    created = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-created",)

    def __str__(self):
        return Truncator(self.text).chars(60)

    def short_text(self):
        return get_truncated_span_from_text(self.text)


class Follow(models.Model):
    """
    Модель Follow для базы данных.

    Обеспечивает систему подписок пользователей друг на друга.
    Объект представляет собой пару пользователей: user подписывается
    на following.

    Поля:
        user — внешний ключ на модель User, каскадное удаление,
        related_name='follower' (кто подписан);
        following — внешний ключ на модель User, каскадное удаление,
        related_name='following' (на кого подписаны).
    """

    user = models.ForeignKey(
        User,
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
        related_name="follower",
    )
    following = models.ForeignKey(
        User,
        verbose_name="Подписан",
        on_delete=models.CASCADE,
        related_name="following",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=["user", "following"],
                                    name="unique_follow"),
        ]
