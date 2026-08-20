from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежа"""
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']