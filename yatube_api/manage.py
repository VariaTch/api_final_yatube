#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    Основная функция для выполнения административных команд Django.

    Устанавливает переменную окружения DJANGO_SETTINGS_MODULE на 'yatube_api.settings',
    затем передаёт аргументы командной строки утилите управления Django.

    Примеры команд:
    - python manage.py runserver
    - python manage.py migrate
    - python manage.py createsuperuser
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yatube_api.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
