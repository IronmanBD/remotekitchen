from django.urls import path
from .views import OrderAPI

urlpatterns = [
    path('orders/', OrderAPI.as_view(), name='orders'),
    path('orders/<int:order_id>/', OrderAPI.as_view(), name='manage-order'),
]