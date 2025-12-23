from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .responses import BaseResponseMixin

User = get_user_model()
# Create your views here.
class RegisterView(BaseResponseMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("VALIDATION ERRORS:", serializer.errors)

            return self.success_response(
                message="Validasi gagal",
                data=serializer.errors,
                code=status.HTTP_400_BAD_REQUEST
            )

        print("VALIDATED DATA:", serializer.validated_data)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return self.success_response(
            data=user_data,
            message="Registrasi berhasil",
            code=status.HTTP_201_CREATED
        )


class LoginWithEmailView(BaseResponseMixin, generics.GenericAPIView) :
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return self.success_response(message = "Email dan password wajib diisi", code=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.select_related('profile').get(email=email)
        except User.DoesNotExist:
            return self.success_response(message = "Email tidak terdaftar", code=status.HTTP_400_BAD_REQUEST)

        # autentikasi manual
        if not user.check_password(password):
            return self.success_response(message = "Password salah", code=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        serializer = LoginSerializer(user)
        data = serializer.data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)


        return self.success_response(
            data=data,
            message="Login berhasil",
            code=status.HTTP_200_OK
        )
    
class GetUserView(BaseResponseMixin, generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)

        
        return self.success_response(
            data=serializer.data,
            message="Data user berhasil diambil",
            code=status.HTTP_200_OK
        )

class LogoutView(BaseResponseMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return self.success_response(message="Refresh token wajib disediakan", code=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return self.success_response(message="Logout berhasil", code=status.HTTP_200_OK)
        except Exception as e:
            return self.success_response(message="Token tidak valid atau sudah kedaluwarsa", code=status.HTTP_400_BAD_REQUEST)