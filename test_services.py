import os
import sys
import django

# Настраиваем Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

# Показываем ключ посимвольно
key = settings.STRIPE_API_KEY
print(f"Длина: {len(key)}")
print(f"Символы: {list(key)}")
print(f"Начинается с 'sk_test_': {key.startswith('sk_test_')}")
print(f"Заканчивается на '4SLf': {key.endswith('4SLf')}")

# Проверяем, нет ли скрытых символов
print(f"Репризентация: {repr(key)}")