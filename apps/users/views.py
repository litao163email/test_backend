from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import LoginSerializer, RefreshSerializer, UserRegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class RefreshView(TokenRefreshView):
    serializer_class = RefreshSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


