from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course', 'owner']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""

    # Поле с количеством уроков
    lessons_count = serializers.SerializerMethodField()

    # Поле со списком всех уроков (используем вложенный сериализатор)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'owner', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        """Метод возвращает количество уроков в курсе"""
        return obj.lessons.count()