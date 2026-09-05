from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычки"""

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action',
            'is_pleasant', 'related_habit', 'periodicity',
            'reward', 'duration', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Валидация на уровне сериализатора
        Вызывается при создании и обновлении привычки
        """
        # 1. Нельзя одновременно заполнять reward и related_habit
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку"
            )

        # 2. Время выполнения не больше 120 секунд
        duration = data.get('duration')
        if duration and duration > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд"
            )

        # 3. У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get('is_pleasant'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError(
                    "Приятная привычка не может иметь вознаграждение или связанную привычку"
                )

        # 4. Связанная привычка должна быть приятной
        related = data.get('related_habit')
        if related:
            # Проверяем, что связанная привычка существует и она приятная
            try:
                related_habit = Habit.objects.get(id=related.id)
                if not related_habit.is_pleasant:
                    raise serializers.ValidationError(
                        "Связанная привычка должна быть приятной"
                    )
            except Habit.DoesNotExist:
                pass

        # 5. Периодичность от 1 до 7 дней
        periodicity = data.get('periodicity')
        if periodicity and (periodicity < 1 or periodicity > 7):
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней"
            )

        return data