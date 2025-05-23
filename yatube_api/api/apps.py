"""
Конфигурация приложения API для проекта Yatube.
Этот модуль определяет класс конфигурации приложения 'api',
который отвечает за настройку и регистрацию приложения в проекте Django.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Конфигурация приложения API для проекта Yatube.
    Определяет настройки конфигурации для приложения 'api',
    которое обрабатывает запросы к API с использованием Django REST Framework.
    """

    name = "api"
