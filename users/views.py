from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser, Payment
from .serializers import CustomUserSerializer, PaymentSerializer
from .filters import PaymentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


# ========== User CRUD ==========
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """Настройка прав доступа для разных действий"""
        if self.action == 'create':
            # Регистрация доступна всем (неавторизованным)
            self.permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            # Остальные действия только для авторизованных
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


# ========== Payment CRUD ==========
class PaymentListCreateView(generics.ListCreateAPIView):
    """Получение списка платежей и создание нового платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [IsAuthenticated]


class PaymentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]