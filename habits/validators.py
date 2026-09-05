from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_habit(data):
    """
    Комплексная валидация привычки
    """
    # 1. Нельзя одновременно заполнять reward и related_habit
    if data.get('reward') and data.get('related_habit'):
        raise ValidationError(
            _("Нельзя одновременно указывать вознаграждение и связанную привычку")
        )

    # 2. Время выполнения не больше 120 секунд
    duration = data.get('duration')
    if duration and duration > 120:
        raise ValidationError(
            _("Время выполнения не должно превышать 120 секунд")
        )

    # 3. У приятной привычки не может быть вознаграждения или связанной привычки
    if data.get('is_pleasant'):
        if data.get('reward') or data.get('related_habit'):
            raise ValidationError(
                _("Приятная привычка не может иметь вознаграждение или связанную привычку")
            )

    # 4. Связанная привычка должна быть приятной
    related = data.get('related_habit')
    if related:
        if not related.is_pleasant:
            raise ValidationError(
                _("Связанная привычка должна быть приятной")
            )

    # 5. Периодичность не реже 1 раза в 7 дней
    periodicity = data.get('periodicity')
    if periodicity and (periodicity < 1 or periodicity > 7):
        raise ValidationError(
            _("Периодичность должна быть от 1 до 7 дней")
        )

    return data