from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from .tasks import send_habit_reminder

User = get_user_model()


class HabitModelTests(TestCase):
    """Тесты для модели привычки"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test123'
        )

    def test_create_habit(self):
        """Тест: создание привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Сделать зарядку',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )
        self.assertEqual(habit.user.email, 'test@example.com')
        self.assertEqual(habit.action, 'Сделать зарядку')

    def test_habit_validation_reward_and_related(self):
        """Тест: нельзя одновременно указывать вознаграждение и связанную привычку"""
        # Создаём приятную привычку
        pleasant = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Приятная привычка',
            is_pleasant=True,
            periodicity=1,
            duration=60
        )

        # Пытаемся создать привычку с reward и related_habit одновременно
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Полезная привычка',
            is_pleasant=False,
            periodicity=1,
            reward='Шоколадка',
            related_habit=pleasant,
            duration=60
        )
        with self.assertRaises(Exception):
            habit.full_clean()

    def test_habit_duration_max_120(self):
        """Тест: время выполнения не больше 120 секунд"""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Сделать зарядку',
            is_pleasant=False,
            periodicity=1,
            duration=150,  # > 120
            is_public=False
        )
        with self.assertRaises(Exception):
            habit.full_clean()


class HabitAPITests(TestCase):
    """Тесты для API привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаём привычку
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Сделать зарядку',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )

    def test_create_habit(self):
        """Тест: создание привычки через API"""
        url = '/api/habits/'
        data = {
            'place': 'Офис',
            'time': '09:00:00',
            'action': 'Пить воду',
            'is_pleasant': False,
            'periodicity': 1,
            'duration': 30,
            'is_public': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habits(self):
        """Тест: получение списка привычек"""
        url = '/api/habits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_habit(self):
        """Тест: обновление привычки"""
        url = f'/api/habits/{self.habit.id}/'
        data = {'action': 'Обновлённая привычка'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Обновлённая привычка')

    def test_delete_habit(self):
        """Тест: удаление привычки"""
        url = f'/api/habits/{self.habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_public_habits_endpoint(self):
        """Тест: получение списка публичных привычек"""
        public_habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='08:00:00',
            action='Прогулка',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=True  # публичная
        )
        url = '/api/habits/public/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_habit(self):
        """Тест: получение одной привычки"""
        url = f'/api/habits/{self.habit.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Сделать зарядку')

    def test_create_habit_duration_too_long(self):
        """Тест: ошибка при создании с duration > 120"""
        url = '/api/habits/'
        data = {
            'place': 'Офис',
            'time': '09:00:00',
            'action': 'Пить воду',
            'is_pleasant': False,
            'periodicity': 1,
            'duration': 150,  # > 120
            'is_public': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_reward_and_related(self):
        """Тест: ошибка при одновременном указании reward и related_habit"""
        # Создаём приятную привычку
        pleasant = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Приятная',
            is_pleasant=True,
            periodicity=1,
            duration=60
        )

        url = '/api/habits/'
        data = {
            'place': 'Офис',
            'time': '09:00:00',
            'action': 'Полезная',
            'is_pleasant': False,
            'periodicity': 1,
            'reward': 'Шоколадка',
            'related_habit': pleasant.id,
            'duration': 60,
            'is_public': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_without_auth(self):
        """Тест: создание привычки без авторизации (должно быть 401)"""
        self.client.force_authenticate(user=None)  # Снимаем авторизацию
        url = '/api/habits/'
        data = {
            'place': 'Офис',
            'time': '09:00:00',
            'action': 'Пить воду',
            'is_pleasant': False,
            'periodicity': 1,
            'duration': 30,
            'is_public': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_pleasant_habit(self):
        """Тест: создание приятной привычки"""
        url = '/api/habits/'
        data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Принять ванну',
            'is_pleasant': True,
            'periodicity': 1,
            'duration': 60,
            'is_public': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_pleasant'], True)

    def test_create_habit_with_related_habit_not_pleasant(self):
        """Тест: ошибка, если связанная привычка не приятная"""
        # Создаём НЕ приятную привычку
        not_pleasant = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Не приятная',
            is_pleasant=False,
            periodicity=1,
            duration=60
        )

        url = '/api/habits/'
        data = {
            'place': 'Офис',
            'time': '09:00:00',
            'action': 'Полезная',
            'is_pleasant': False,
            'periodicity': 1,
            'related_habit': not_pleasant.id,
            'duration': 60,
            'is_public': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HabitPermissionsTests(TestCase):
    """Тесты для прав доступа"""

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='test123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='test123'
        )
        self.client = APIClient()

        # Создаём привычку от user1
        self.habit = Habit.objects.create(
            user=self.user1,
            place='Дом',
            time='08:00:00',
            action='Привычка user1',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )

    def test_user_cannot_edit_others_habit(self):
        """Тест: пользователь не может редактировать чужую привычку"""
        self.client.force_authenticate(user=self.user2)
        url = f'/api/habits/{self.habit.id}/'
        data = {'action': 'Попытка изменить'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_others_habit(self):
        """Тест: пользователь не может удалять чужую привычку"""
        self.client.force_authenticate(user=self.user2)
        url = f'/api/habits/{self.habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HabitTasksTests(TestCase):
    """Тесты для Celery-задач"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test123'
        )

    def test_send_habit_reminder(self):
        """Тест: отправка напоминаний (логирование)"""
        # Создаём привычку на текущее время
        now = timezone.now()
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=now.time(),
            action='Тестовая привычка',
            is_pleasant=False,
            periodicity=1,
            duration=60,
            is_public=False
        )

        # Запускаем задачу
        result = send_habit_reminder()
        self.assertIsNotNone(result)

