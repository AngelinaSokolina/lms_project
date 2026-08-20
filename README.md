# LMS System (Learning Management System)

API для платформы онлайн-обучения, где пользователи могут создавать курсы и уроки.

## Установка и запуск

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

## Примеры запросов

### Создание курса

```json
POST /api/courses/
{
    "name": "Python для начинающих",
    "description": "Полный курс по Python с нуля"
}
```

### Создание урока

```json
POST /api/lessons/
{
    "name": "Установка Python",
    "description": "Как установить Python на Windows/Mac",
    "video_url": "https://youtube.com/watch?v=example",
    "course": 1
}
```

## Модели данных

### Пользователь (CustomUser)
- email (логин)
- телефон
- город
- аватарка

### Курс (Course)
- название
- превью (картинка)
- описание

### Урок (Lesson)
- название
- описание
- превью (картинка)
- ссылка на видео
- курс (связь с Course)

