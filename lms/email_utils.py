from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription


def send_course_update_email_sync(course_id):
    """Отправляет письма подписчикам (синхронно)"""
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        if not subscriptions.exists():
            print(f"Нет подписчиков для курса {course.name}")
            return

        recipient_list = [sub.user.email for sub in subscriptions]

        send_mail(
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

        print(f"Письма отправлены {len(recipient_list)} подписчикам курса {course.name}")

    except Course.DoesNotExist:
        print(f"Курс с ID {course_id} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")