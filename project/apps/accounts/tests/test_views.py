import uuid
from unittest.mock import MagicMock, patch

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.test import APITestCase

from ..models import PasswordResetToken, User
from ..serializers import (
    EmailSerializer,
    PasswordResetSerializer,
    PasswordResetTokenSerializer,
    PasswordSerializer,
    ProfileSerializer,
    SignupSerializer,
)
from ..views import (
    EmailView,
    PasswordResetTokenView,
    PasswordResetView,
    PasswordView,
    ProfileView,
    SignupView,
)


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


class PasswordResetTokenViewTests(APITestCase):
    def setUp(self):
        self.view = PasswordResetTokenView

    def test_subclass(self):
        self.assertTrue(issubclass(self.view, generics.CreateAPIView))

    def test_permission_classes(self):
        self.assertEqual(self.view.permission_classes, (AllowAny,))

    def test_serializer_class(self):
        self.assertEqual(self.view.serializer_class, PasswordResetTokenSerializer)


class PasswordResetTokenViewPostTests(APITestCase):
    def setUp(self):
        self.url = '/accounts/password/reset/'
        self.user = User.objects.create_user('u@test.com', 'foo123')

    @patch('project.apps.accounts.serializers.SendGridEmail')
    def test_201_created(self, SendGridEmail):
        response = self.client.post(self.url, data={'email': 'u@test.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {})
        self.assertEqual(PasswordResetToken.objects.count(), 1)
        token = PasswordResetToken.objects.first()
        self.assertEqual(token.user, self.user)

    def test_201_not_created(self):
        response = self.client.post(self.url, data={'email': 'foo@bar.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PasswordResetToken.objects.count(), 0)
        self.assertEqual(response.data, {})


class PasswordResetViewTests(APITestCase):
    def setUp(self):
        self.view = PasswordResetView

    def test_subclass(self):
        self.assertTrue(issubclass(self.view, generics.UpdateAPIView))

    def test_permission_classes(self):
        self.assertEqual(self.view.permission_classes, (AllowAny,))

    def test_serializer_class(self):
        self.assertEqual(self.view.serializer_class, PasswordResetSerializer)

    def test_queryset(self):
        self.assertEqual(self.view.queryset, PasswordResetToken)

    def test_http_method_names(self):
        self.assertEqual(self.view.http_method_names, ['put'])


class PasswordResetViewPutTests(APITestCase):
    def setUp(self):
        self.url = '/accounts/password/reset/{}/'
        self.user = User.objects.create_user('u@test.com', 'foo123')
        self.token = PasswordResetToken.objects.create(user=self.user)
        self.data = {
            'password': 'bar321',
            'password_confirm': 'bar321',
        }

    def test_200(self):
        response = self.client.put(self.url.format(self.token.id), data=self.data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.data['password']))
        self.token.refresh_from_db()
        self.assertFalse(self.token.valid)

    def test_400_distinct_passwords(self):
        self.data['password'] = 'foobar123!'
        response = self.client.put(self.url.format(self.token.id), data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['non_field_errors'][0].code, 'invalid')

    def test_400_missing_data(self):
        response = self.client.put(self.url.format(self.token.id), data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data['password'][0].code, 'required')
        self.assertEqual(response.data['password_confirm'][0].code, 'required')

    def test_404(self):
        response = self.client.put(self.url.format(uuid.uuid4()), data=self.data)
        self.assertEqual(response.status_code, 403)


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
