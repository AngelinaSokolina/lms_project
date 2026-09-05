from django.db import models
from django.conf import settings
from .validators import validate_habit


class Habit(models.Model):
    """Модель привычки"""

    # Поля из задания
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=200, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        help_text='Может быть только приятной привычкой'
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность в днях',
        help_text='Не реже 1 раза в 7 дней'
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Вознаграждение')
    duration = models.PositiveSmallIntegerField(
        verbose_name='Время на выполнение в секундах',
        help_text='Не больше 120 секунд'
    )
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    # Автоматические поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.action}"

    def clean(self):
        """Вызов валидации при сохранении"""
        validate_habit({
            'reward': self.reward,
            'related_habit': self.related_habit,
            'duration': self.duration,
            'is_pleasant': self.is_pleasant,
            'periodicity': self.periodicity,
        })

    def save(self, *args, **kwargs):
        """Переопределяем save для вызова clean"""
        self.full_clean()
        super().save(*args, **kwargs)