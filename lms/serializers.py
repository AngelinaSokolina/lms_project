from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url



class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url], required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course', 'owner']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'owner', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']