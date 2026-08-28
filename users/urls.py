from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentCreateView, PaymentRetrieveUpdateDeleteView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('payment/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDeleteView.as_view(), name='payment-retrieve-update-delete'),
]