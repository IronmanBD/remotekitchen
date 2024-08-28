from django.urls import path
from .views import PaymentAPI, StripeWebhookAPI

urlpatterns = [
    path('payments/<int:order_id>/', PaymentAPI.as_view(), name = 'payment'),
    path('payments/stripe/webhook/', StripeWebhookAPI.as_view(), name='stripe-webhook'),
]