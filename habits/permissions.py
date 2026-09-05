from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Проверка, является ли пользователь владельцем привычки.
    Используется для проверки прав на редактирование и удаление.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяем, что объект принадлежит текущему пользователю.
        """
        # Если пользователь не авторизован — доступ запрещён
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверяем, что владелец привычки совпадает с текущим пользователем
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает просмотр всем авторизованным,
    но редактирование и удаление только владельцу.
    """

    def has_permission(self, request, view):
        """
        Проверяем, что пользователь авторизован.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Проверяем, что пользователь является владельцем.
        """
        # Безопасные методы (GET, HEAD, OPTIONS) разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Остальные методы (POST, PUT, PATCH, DELETE) — только владельцу
        return obj.user == request.user