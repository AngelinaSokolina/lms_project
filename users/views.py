from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter


class PaymentListCreateView(generics.ListCreateAPIView):
    """Получение списка платежей и создание нового платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # по умолчанию сортировка по убыванию даты


class PaymentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer