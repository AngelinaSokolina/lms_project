from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonTests(TestCase):
    """Тесты для уроков"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='user@test.ru',
            password='test123'
        )
        self.moderator = User.objects.create_user(
            email='moderator@test.ru',
            password='test123'
        )
        # Добавляем модератора в группу
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator.groups.add(group)

        # Создаем курс
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            name='Тестовый урок',
            description='Описание урока',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        # Настраиваем клиенты
        self.client = APIClient()

    def test_create_lesson_by_user(self):
        """Тест: обычный пользователь может создать урок"""
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list-create')
        data = {
            'name': 'Новый урок',
            'description': 'Описание',
            'video_url': 'https://www.youtube.com/watch?v=new',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_by_moderator(self):
        """Тест: модератор НЕ может создать урок"""
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lesson-list-create')
        data = {
            'name': 'Урок от модератора',
            'description': 'Описание',
            'video_url': 'https://www.youtube.com/watch?v=new',
            'course': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_update_lesson_by_owner(self):
        """Тест: владелец может обновить свой урок"""
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-retrieve-update-delete', args=[self.lesson.id])
        data = {'name': 'Обновленный урок'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Обновленный урок')

    def test_update_lesson_by_moderator(self):
        """Тест: модератор может обновить чужой урок"""
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lesson-retrieve-update-delete', args=[self.lesson.id])
        data = {'name': 'Изменено модератором'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Изменено модератором')

    def test_delete_lesson_by_owner(self):
        """Тест: владелец может удалить свой урок"""
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-retrieve-update-delete', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_by_moderator(self):
        """Тест: модератор НЕ может удалить урок"""
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lesson-retrieve-update-delete', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)


class SubscriptionTests(TestCase):
    """Тесты для подписок"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.ru',
            password='test123'
        )
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание',
            owner=self.user
        )
        self.client = APIClient()

    def test_create_subscription(self):
        """Тест: создание подписки"""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscription')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_delete_subscription(self):
        """Тест: удаление подписки"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        url = reverse('subscription')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())