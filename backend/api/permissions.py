"""Write your api app permissions here."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorPermissionOrReadOnly(BasePermission):
    """Разрешение на изменение постов только для автора или чтение."""

    def has_object_permission(self, request, view, obj):
        """
        Сравнение автора объекта c текущим пользователем.

        Или пользователь является автором.
        """
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
