# LMS System (Learning Management System)

API для платформы онлайн-обучения, где пользователи могут создавать курсы и уроки.

## Запуск через Docker (рекомендуемый способ)

### 1. Скопируйте файл с переменными окружения:

```bash
cp .env.docker .env
```
### 2. Соберите и запустите контейнеры:

```bash
docker compose up -d --build
```
### 3. Выполните миграции:

```bash
docker compose exec web python manage.py migrate
```
### 4. Создайте суперпользователя:

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Проект доступен по адресу:

```bash
http://localhost:8000
```

### 6. Остановка контейнеров:

```bash
docker compose down
```

## Структура Docker-контейнеров

| Сервис | Контейнер | Назначение |
|--------|-----------|------------|
| **db** | `lms_db` | PostgreSQL — база данных |
| **redis** | `lms_redis` | Redis — брокер для Celery |
| **web** | `lms_web` | Django — основное приложение |
| **celery** | `lms_celery` | Celery worker — выполнение фоновых задач |
| **celery-beat** | `lms_celery_beat` | Celery beat — запуск задач по расписанию |

## Установка и альтернативный запуск (без Docker)

### 1. Клонирование репозитория

```bash
git clone <url-вашего-репозитория>
cd lms_project
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv venv
source venv/bin/activate      # для Mac/Linux
venv\Scripts\activate         # для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## API Эндпоинты


### Авторизация

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /api/token/| Получение JWT-токенов |
| POST | /api/token/refresh/ | Обновление access-токена |


### Курсы (Course) — ViewSet

| Метод | URL | Описание |
|-------|-----|----------|
| GET | /api/courses/ | Список всех курсов |
| POST | /api/courses/ | Создание курса |
| GET | /api/courses/{id}/ | Получение одного курса |
| PUT | /api/courses/{id}/ | Полное обновление курса |
| PATCH | /api/courses/{id}/ | Частичное обновление курса |
| DELETE | /api/courses/{id}/ | Удаление курса |

### Уроки (Lesson) — Generic-классы

| Метод | URL | Описание |
|-------|-----|----------|
| GET | /api/lessons/ | Список всех уроков |
| POST | /api/lessons/ | Создание урока |
| GET | /api/lessons/{id}/ | Получение одного урока |
| PUT | /api/lessons/{id}/ | Полное обновление урока |
| PATCH | /api/lessons/{id}/ | Частичное обновление урока |
| DELETE | /api/lessons/{id}/ | Удаление урока |


### Привычки (Habits)
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/habits/` | Список своих привычек |
| GET | `/api/habits/public/` | Список публичных привычек |
| POST | `/api/habits/` | Создание привычки |
| GET | `/api/habits/{id}/` | Получение привычки |
| PUT/PATCH | `/api/habits/{id}/` | Редактирование привычки |
| DELETE | `/api/habits/{id}/` | Удаление привычки |

---

### Подписки
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/subscription/` | Создать или удалить подписку на курс |

---

### Оплата (Stripe)
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/payment/create/` | Создание платежа через Stripe |



## Примеры запросов

### Создание курса

```json
POST /api/courses/
{
    "name": "Python для начинающих",
    "description": "Полный курс по Python с нуля"
}
```

## Документация API
После запуска сервера документация доступна по адресам:

Swagger UI: http://localhost:8000/docs/

ReDoc: http://localhost:8000/redoc/


## Запуск тестов
Все тесты
```bash
python manage.py test
```
Тесты привычек с покрытием
```bash
coverage run manage.py test habits
coverage report
```

