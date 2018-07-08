from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import EmailSerializer, PasswordSerializer, SignupSerializer


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
