from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Является ли пользователь автором объекта.
    """
    # def has_permission(self, request, view):
    #     # Разрешаем только аутентифицированным пользователям
    #     return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить изменение и удаление только автору объекта
        return obj.author == request.user


class NonAuthorizedUserIsNotAllowed(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
