from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


# ========== Course - ViewSet ==========
class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# ========== Lesson - Generic классы ==========
class LessonListCreateView(generics.ListCreateAPIView):
    """Получение списка уроков и создание нового урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer