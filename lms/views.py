from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwner, IsModerator


# ========== Course - ViewSet ==========
class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Настройка прав доступа для разных действий"""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """При создании курса автоматически назначаем владельца"""
        serializer.save(owner=self.request.user)


# ========== Lesson - Generic классы ==========
class LessonListCreateView(generics.ListCreateAPIView):
    """Получение списка уроков и создание нового урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """Настройка прав доступа для разных действий"""
        if self.request.method == 'POST':
            # Создание: только авторизованные, НЕ модераторы
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            # Просмотр списка: только авторизованные
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """При создании урока автоматически назначаем владельца"""
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """Настройка прав доступа для разных действий"""
        if self.request.method == 'GET':
            # Просмотр: только авторизованные
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH']:
            # Редактирование: авторизованные И (модератор ИЛИ владелец)
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.request.method == 'DELETE':
            # Удаление: только владелец
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]