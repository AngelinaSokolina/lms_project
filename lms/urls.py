from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDeleteView

# Роутер для ViewSet (Course)
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    # Маршруты для Course через ViewSet (автоматически создаются все CRUD)
    path('', include(router.urls)),

    # Маршруты для Lesson через Generic классы
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDeleteView.as_view(), name='lesson-retrieve-update-delete'),
]