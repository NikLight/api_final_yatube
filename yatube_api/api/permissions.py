from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает доступ для аутентифицированных пользователей и безопасные методы.
    Позволяет изменение и удаление только автору объекта.
    """
    def has_permission(self, request, view):
        # Разрешаем доступ ко всем безопасным методам и аутентифицированным пользователям
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы и доступ автору объекта для изменений
        return request.method in permissions.SAFE_METHODS or obj.author == request.user
