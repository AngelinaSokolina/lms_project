from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDeleteView, SubscriptionView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDeleteView.as_view(), name='lesson-retrieve-update-delete'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
]