import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription

logger = logging.getLogger(__name__)


@shared_task
def send_course_update_email(course_id):
    """Отправляет письма всем подписчикам курса об обновлении"""
    logger.info(f"Задача send_course_update_email запущена для курса ID: {course_id}")

    try:
        course = Course.objects.get(id=course_id)
        logger.info(f"Курс найден: {course.name}")

        subscriptions = Subscription.objects.filter(course=course)
        logger.info(f"Найдено подписок: {subscriptions.count()}")

        if not subscriptions.exists():
            logger.info(f"Нет подписчиков для курса {course.name}")
            return f"Нет подписчиков для курса {course.name}"

        recipient_list = [sub.user.email for sub in subscriptions]
        logger.info(f"Список получателей: {recipient_list}")

        result = send_mail(
            subject=f"Обновление курса: {course.name}",
            message=f"""
Здравствуйте!

Курс "{course.name}" был обновлён.
Зайдите на платформу, чтобы ознакомиться с новыми материалами.

Ссылка: http://127.0.0.1:8000/api/courses/{course.id}/

С уважением,
Команда LMS
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        logger.info(f"Письма отправлены {len(recipient_list)} подписчикам")
        return f"Письма отправлены {len(recipient_list)} подписчикам курса {course.name}"

    except Course.DoesNotExist:
        logger.error(f"Курс с ID {course_id} не найден")
        return f"Курс с ID {course_id} не найден"
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return f"Ошибка: {str(e)}"