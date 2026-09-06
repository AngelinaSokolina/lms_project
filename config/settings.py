import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

# Загружаем переменные окружения из файла .env
load_dotenv()

# Указывает на текущую/корневую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секреты/ключ приложения
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# IP и домены, которые имеют доступ в приложение
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'django_celery_beat',
    'drf_yasg',
    'corsheaders',
    'users',
    'lms',
    'habits',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Настройки для базы данных

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #  имя вашей базы данных, получаемое из переменной окружения DATABASE_NAME
        'NAME': os.getenv('NAME', 'django_project'),
        # имя пользователя PostgreSQL, получаемое из переменной окружения DATABASE_USER
        'USER': os.getenv('USER', 'postgres'),
        # пароль пользователя PostgreSQL, получаемый из переменной окружения DATABASE_PASSWORD
        'PASSWORD': os.getenv('PASSWORD', 'postgres'),
        # адрес сервера базы данных, получаемый из переменной окружения DATABASE_HOST
        'HOST': os.getenv('HOST', 'localhost'),
        # порт, на котором работает PostgreSQL, обычно 5432, получаемый из переменной окружения DATABASE_PORT
        'PORT': os.getenv('PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Кастомная модель пользователя
AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Путь директорий на диске, из которых мы загружаем статистические файлы
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


#после входа → на главную
LOGIN_REDIRECT_URL = '/'
#после выхода → на главную
LOGOUT_REDIRECT_URL = '/'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Настройки Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # <-- ВСЕ эндпоинты требуют авторизации по умолчанию
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Stripe настройки (загружаются из .env)
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')


# Celery настройки
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379')
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 30 * 60

# Email настройки
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Telegram настройки
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# CORS настройки
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')


