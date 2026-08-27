from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwner, IsModerator
from .paginators import CoursePaginator, LessonPaginator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404





# ========== Course - ViewSet ==========
class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator  # <--  пагинатор

    def get_permissions(self):
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
        serializer.save(owner=self.request.user)


# ========== Lesson - Generic классы ==========
class LessonListCreateView(generics.ListCreateAPIView):
    """Получение списка уроков и создание нового урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator  # <-- пагинатор

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]


class SubscriptionView(APIView):
    """Эндпоинт для управления подписками"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Создание или удаление подписки"""
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Необходимо указать course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, существует ли курс
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            # Если есть — удаляем
            subscription.delete()
            message = 'Подписка удалена'
        else:
            # Если нет — создаём
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)