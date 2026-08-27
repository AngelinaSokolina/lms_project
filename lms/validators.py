import re
from rest_framework import serializers


def validate_youtube_url(value):
    """
    Валидатор проверяет, что ссылка ведёт на youtube.com
    """
    # Проверяем, что ссылка содержит youtube.com или youtu.be
    if not value:
        return value  # Пустое поле пропускаем (оно необязательное)

    # Регулярное выражение для проверки youtube-ссылок
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/'

    if not re.search(youtube_pattern, value):
        raise serializers.ValidationError(
            "Ссылка должна вести на видео с youtube.com. "
            "Ссылки на сторонние ресурсы запрещены."
        )

    return value