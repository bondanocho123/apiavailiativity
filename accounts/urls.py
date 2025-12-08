# users/urls.py
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginWithEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login-email/', LoginWithEmailView.as_view(), name='login-email'),
]
