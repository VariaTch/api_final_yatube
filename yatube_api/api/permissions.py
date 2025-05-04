"""
Права доступа для объектов в API Yatube.
Этот модуль содержит настраиваемые классы прав доступа (permissions),
используемые для ограничения прав на изменение объектов.
"""

from rest_framework import permissions


class IsObjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ, если пользователь — автор объекта или
    запрос безопасный.
    Безопасные методы (SAFE_METHODS) — это GET, HEAD, OPTIONS.
    В остальных случаях редактировать или удалять объект может
    только его автор.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет права на объект.
        Возвращает True, если метод безопасный (чтение),
        либо если пользователь является автором объекта.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and obj.author == request.user
