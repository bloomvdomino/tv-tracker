from unittest.mock import MagicMock

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.test import APITestCase

from ..models import User
from ..serializers import (EmailSerializer, PasswordSerializer,
                           ProfileSerializer, SignupSerializer)
from ..views import EmailView, PasswordView, ProfileView, SignupView


class SignupViewTests(APITestCase):
    def setUp(self):
        self.view = SignupView

    def test_subclass(self):
        self.assertTrue(issubclass(self.view, generics.CreateAPIView))

    def test_permission_classes(self):
        self.assertEqual(self.view.permission_classes, (AllowAny,))

    def test_serializer_class(self):
        self.assertEqual(self.view.serializer_class, SignupSerializer)


class EmailViewTests(APITestCase):
    def setUp(self):
        self.view = EmailView

    def test_subclass(self):
        self.assertTrue(issubclass(self.view, generics.UpdateAPIView))

    def test_permission_classes(self):
        self.assertEqual(self.view.permission_classes, [IsAuthenticated])

    def test_serializer_class(self):
        self.assertEqual(self.view.serializer_class, EmailSerializer)

    def test_http_method_names(self):
        self.assertEqual(self.view.http_method_names, ['put'])

    def test_get_object(self):
        user = User()
        view = self.view()
        view.request = MagicMock(user=user)
        self.assertEqual(view.get_object(), user)


class PasswordViewTests(APITestCase):
    def setUp(self):
        self.view = PasswordView

    def test_subclass(self):
        self.assertTrue(issubclass(self.view, generics.UpdateAPIView))

    def test_permission_classes(self):
        self.assertEqual(self.view.permission_classes, [IsAuthenticated])

    def test_serializer_class(self):
        self.assertEqual(self.view.serializer_class, PasswordSerializer)

    def test_http_method_names(self):
        self.assertEqual(self.view.http_method_names, ['put'])

    def test_get_object(self):
        user = User()
        view = self.view()
        view.request = MagicMock(user=user)
        self.assertEqual(view.get_object(), user)


class ProfileViewTests(APITestCase):
    def setUp(self):
        self.view = ProfileView

    def test_subclass(self):
        self.assertTrue(issubclass(self.view, generics.RetrieveAPIView))

    def test_permission_classes(self):
        self.assertEqual(self.view.permission_classes, [IsAuthenticated])

    def test_serializer_class(self):
        self.assertEqual(self.view.serializer_class, ProfileSerializer)

    def test_get_object(self):
        user = User()
        view = self.view()
        view.request = MagicMock(user=user)
        self.assertEqual(view.get_object(), user)
