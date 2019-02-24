from django.contrib.auth import views
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import PasswordResetToken
from .serializers import (
    EmailSerializer,
    PasswordResetSerializer,
    PasswordResetTokenSerializer,
    PasswordSerializer,
    ProfileSerializer,
    SignupSerializer,
)


class SignupView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


class EmailView(generics.UpdateAPIView):
    serializer_class = EmailSerializer
    http_method_names = ['put']

    def get_object(self):
        return self.request.user


class PasswordView(generics.UpdateAPIView):
    serializer_class = PasswordSerializer
    http_method_names = ['put']

    def get_object(self):
        return self.request.user


class PasswordResetTokenView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetTokenSerializer


class PasswordResetView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer
    queryset = PasswordResetToken
    http_method_names = ['put']


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class V2SignupView(TemplateView):
    template_name = 'accounts/signup.html'


class V2LoginView(views.LoginView):
    template_name = 'accounts/login.html'


class V2ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
