from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверка, является ли пользователь модератором"""

    def has_permission(self, request, view):
        # Если пользователь не авторизован — доступ запрещен
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверяем, есть ли пользователь в группе moderators
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        # Проверяем, что у объекта есть поле owner и оно совпадает с текущим пользователем
        return hasattr(obj, 'owner') and obj.owner == request.user