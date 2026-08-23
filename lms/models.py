from django.db import models
from django.conf import settings


class Course(models.Model):
    """Модель курса"""
    name = models.CharField(max_length=200, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/previews/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    # Владелец курса
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Модель урока"""
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    preview = models.ImageField(upload_to='lessons/previews/', blank=True, null=True, verbose_name='Превью')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')

    # Связь с курсом (один курс - много уроков)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )

    # Владелец урока
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons',
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'