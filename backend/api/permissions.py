"""Write your api app permissions here."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorPermissionOrReadOnly(BasePermission):
    """Разрешение на изменение постов только для автора или чтение."""

    message = 'У вас нет прав на эту операцию.'

    def has_permission(self, request, view):
        """Проверка метод запроса безопасен или пользователь авторизован."""
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """
        Сравнение автора объекта c текущим пользователем.

        Или пользователь является автором.
        """
        return (obj.author == request.user or
                request.method in SAFE_METHODS)
