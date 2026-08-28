from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import CustomUser, Payment
from .serializers import CustomUserSerializer, PaymentSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_checkout_session
from lms.models import Course


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


# ========== Payment Create ==========
class PaymentCreateView(APIView):
    """Создание платежа через Stripe"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'Необходимо указать course_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        # Создаем продукт в Stripe
        product = create_stripe_product(course.name)
        if not product:
            return Response(
                {'error': 'Не удалось создать продукт в Stripe'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Создаем цену в Stripe (сумма из курса, но можно сделать фиксированную)
        amount = 1000  # 1000 руб.
        price = create_stripe_price(amount, product.id)
        if not price:
            return Response(
                {'error': 'Не удалось создать цену в Stripe'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Создаем сессию оплаты
        session = create_stripe_checkout_session(price.id)
        if not session:
            return Response(
                {'error': 'Не удалось создать сессию оплаты'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Сохраняем платеж в БД
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=amount,
            payment_method='transfer',
            stripe_product_id=product.id,
            stripe_price_id=price.id,
            stripe_session_id=session.id,
            stripe_payment_url=session.url,
            status='pending'
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]