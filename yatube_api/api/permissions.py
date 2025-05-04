from rest_framework import permissions


class IsObjectAuthorOrReadOnly(permissions.BasePermission):
    """Grant access if user is object author OR method is safe."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and obj.author == request.user