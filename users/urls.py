from django.urls import path
from .views import PaymentListCreateView, PaymentRetrieveUpdateDeleteView

urlpatterns = [
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDeleteView.as_view(), name='payment-retrieve-update-delete'),
]