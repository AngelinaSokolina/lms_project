from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца
    """
    # Вычисляем дату: сейчас минус 30 дней
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца
    inactive_users = CustomUser.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    )

    count = inactive_users.count()

    if count > 0:
        # Блокируем их (батчем, а не по одному)
        inactive_users.update(is_active=False)
        print(f"Заблокировано {count} неактивных пользователей")
    else:
        print("Неактивных пользователей не найдено")

    return f"Заблокировано {count} пользователей"