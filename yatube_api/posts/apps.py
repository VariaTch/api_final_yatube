from django.apps import AppConfig


class PostsConfig(AppConfig):
    """
    Конфигурация приложения "Публикации" для Django.

    Этот класс настраивает параметры приложения "posts" и задает имя приложения,
    а также его отображаемое имя в административной панели Django.
    """
    name = "posts"
    verbose_name = "Публикации"

