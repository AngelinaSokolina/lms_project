from rest_framework import serializers
from .models import CustomUser, Payment


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    def create(self, validated_data):
        """Переопределяем метод create для хеширования пароля"""
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)  # Хешируем пароль
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'is_active', 'is_staff', 'password']
        read_only_fields = ['is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}  # Пароль не выводится в ответе
        }


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежа"""
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'payment_date', 'course', 'lesson',
                  'amount', 'payment_method', 'stripe_payment_url', 'status']
        read_only_fields = ['stripe_payment_url', 'status']
