from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    """Фильтр для платежей"""
    # Фильтрация по курсу и уроку
    course = filters.NumberFilter(field_name='course__id')
    lesson = filters.NumberFilter(field_name='lesson__id')

    # Фильтрация по способу оплаты
    payment_method = filters.ChoiceFilter(choices=Payment.PaymentMethod.choices)

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']