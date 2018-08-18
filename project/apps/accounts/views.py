from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import PasswordResetToken
from .serializers import (EmailSerializer, PasswordResetSerializer,
                          PasswordResetTokenSerializer, PasswordSerializer,
                          ProfileSerializer, SignupSerializer)


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
