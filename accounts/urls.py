# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginWithEmailView, RegisterView, LogoutView, GetUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login-email/', LoginWithEmailView.as_view(), name='login-email'),
    path('me/', GetUserView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
