from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistrationAPI, LoginAPI, LogoutAPI

urlpatterns = [
    path('register/', RegistrationAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutAPI.as_view(), name='logout')
]