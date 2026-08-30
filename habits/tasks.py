import requests
from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from .models import Habit


@shared_task
def send_habit_reminder():
    """
    Отправляет напоминания о привычках, которые нужно выполнить сейчас.
    Запускается периодически (например, каждый час).
    """
    # Получаем текущее время
    now = timezone.now()
    current_time = now.time()

    # Находим привычки, которые нужно выполнить в этот час
    # Проверяем, что текущее время соответствует времени привычки
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        is_pleasant=False  # Напоминаем только о полезных привычках
    )

    sent_count = 0

    for habit in habits:
        # Проверяем, что пользователь не заблокирован
        if not habit.user.is_active:
            continue

        # Получаем chat_id пользователя (если он указан)
        chat_id = getattr(habit.user, 'telegram_chat_id', None)
        if not chat_id:
            continue

        # Формируем сообщение
        message = f"""
🔔 Напоминание о привычке!

Действие: {habit.action}
Место: {habit.place}
Время: {habit.time.strftime('%H:%M')}

💪 Не забудьте выполнить!
        """

        # Отправляем сообщение через Telegram API
        try:
            send_telegram_message(chat_id, message)
            sent_count += 1
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

    return f"Отправлено {sent_count} напоминаний"


def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение в Telegram через API бота.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()