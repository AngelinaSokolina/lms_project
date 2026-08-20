from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""
    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description']


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course']