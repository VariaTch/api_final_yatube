from django.contrib import admin

from .models import Group, Post, Comment, Follow

# Настройка для отображения пустых значений в админке
admin.site.empty_value_display = "-"


class PostInline(admin.TabularInline):
    """
    Вспомогательное отображение постов, связанных с группой, в админке.

    Используется для отображения списка постов внутри страницы
    редактирования группы.
    """
    model = Post
    extra = 1


class CommentInline(admin.TabularInline):
    """
    Вспомогательное отображение комментариев, связанных с постом, в админке.

    Используется для отображения списка комментариев внутри страницы
    редактирования поста.
    """
    model = Comment
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Настройка отображения и редактирования групп в админке.

    Включает отображение полей, настройку поиска и возможность
    добавления постов.
    """
    list_display = (
        "pk",
        "title",
        "slug",
        "short_description",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    search_fields = (
        "title",
        "slug",
    )
    list_display_links = ("title",)
    inlines = (PostInline,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Настройка отображения и редактирования постов в админке.

    Включает отображение полей, фильтрацию по дате, автору и группе,
    а также возможность добавления комментариев.
    """
    list_display = (
        "pk",
        "short_text",
        "author",
        "group",
        "image",
        "pub_date",
    )
    list_filter = (
        "pub_date",
        "author",
        "group",
    )
    search_fields = ("text",)
    list_display_links = ("short_text",)
    inlines = (CommentInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройка отображения и редактирования комментариев в админке.

    Включает отображение полей, фильтрацию по дате создания, автору и посту.
    """
    list_display = (
        "pk",
        "short_text",
        "author",
        "post",
        "created",
    )
    list_filter = (
        "created",
        "author",
        "post",
    )
    search_fields = ("text",)
    list_display_links = ("short_text",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Настройка отображения и редактирования подписок в админке.

    Включает отображение полей, фильтрацию по пользователю и
    подписанному пользователю.
    """
    list_display = (
        "pk",
        "user",
        "following",
    )
    list_filter = (
        "user",
        "following",
    )
    list_display_links = ("user", "following")
