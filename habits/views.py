from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import models
from .models import Habit
from .serializers import HabitSerializer
from .paginators import HabitPaginator
from .permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для управления привычками"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """
        Возвращает привычки текущего пользователя и публичные привычки других
        """
        user = self.request.user
        return Habit.objects.filter(
            models.Q(user=user) | models.Q(is_public=True)
        ).distinct()

    def perform_create(self, serializer):
        """При создании привычки автоматически назначаем владельца"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='public')
    def public_habits(self, request):
        """
        Эндпоинт для получения списка публичных привычек
        """
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """
        Настройка прав доступа для разных действий
        """
        if self.action in ['list', 'retrieve', 'public_habits']:
            # Просмотр: только авторизованные
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Создание, изменение, удаление: авторизованные и владельцы
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]