from unittest.mock import PropertyMock, patch

from django.contrib.auth.password_validation import validate_password
from django.test import TestCase
from rest_framework import serializers

from project.apps.accounts.models import User
from project.apps.emails.models import SendGridEmail

from ..models import PasswordResetToken
from ..serializers import (CurrentPasswordSerializer, EmailSerializer,
                           PasswordConfirmSerializer, PasswordField,
                           PasswordResetSerializer,
                           PasswordResetTokenSerializer, PasswordSerializer,
                           ProfileSerializer, SignupSerializer,
                           TokenSerializer)


class PasswordFieldTests(TestCase):
    def setUp(self):
        self.field = PasswordField

    def test_subclass(self):
        self.assertTrue(issubclass(self.field, serializers.CharField))

    def test__init__(self):
        field = self.field()
        self.assertTrue(field.write_only)
        self.assertIn(validate_password, field.validators)


class PasswordConfirmSerializerTests(TestCase):
    def setUp(self):
        self.serializer = PasswordConfirmSerializer

    def test_subclass(self):
        self.assertTrue(issubclass(self.serializer, serializers.Serializer))

    def test_password_confirm(self):
        field = self.serializer._declared_fields['password_confirm']
        self.assertEqual(type(field), serializers.CharField)
        self.assertTrue(field.write_only)

    def test_validate_invalid(self):
        data = {
            'password': '123',
            'password_confirm': '321'
        }
        with self.assertRaises(serializers.ValidationError) as e:
            self.serializer().validate(data)
        self.assertEqual(str(e.exception.detail[0]), 'Incorrect password confirmation.')

    def test_validate_valid(self):
        data = {
            'password': '123',
            'password_confirm': '123'
        }
        self.assertEqual(self.serializer().validate(data), data)


class CurrentPasswordSerializerTests(TestCase):
    def setUp(self):
        self.serializer = CurrentPasswordSerializer

    def test_subclass(self):
        self.assertTrue(issubclass(self.serializer, serializers.Serializer))

    def test_current_password(self):
        field = self.serializer._declared_fields['current_password']
        self.assertEqual(type(field), serializers.CharField)
        self.assertTrue(field.write_only)

    def test_validate_current_password_invalid(self):
        user = User.objects.create_user('u@test.com', 'foo123')
        with self.assertRaises(serializers.ValidationError) as e:
            self.serializer(instance=user).validate_current_password('foo')
        self.assertEqual(str(e.exception.detail[0]), 'Incorrect current password.')

    def test_validate_current_password_valid(self):
        user = User.objects.create_user('u@test.com', 'foo123')
        value = self.serializer(instance=user).validate_current_password('foo123')
        self.assertEqual(value, 'foo123')


class TokenSerializerTests(TestCase):
    def setUp(self):
        self.serializer = TokenSerializer

    def test_subclass(self):
        self.assertTrue(issubclass(self.serializer, serializers.Serializer))

    def test_token(self):
        field = self.serializer._declared_fields['token']
        self.assertEqual(type(field), serializers.SerializerMethodField)

    @patch('project.apps.accounts.serializers.create_token', return_value='foobar')
    def test_get_token(self, create_token):
        user = User()
        token = self.serializer().get_token(user)
        self.assertEqual(token, 'foobar')
        create_token.assert_called_once_with(user)


class SignupSerializerTests(TestCase):
    def setUp(self):
        self.serializer = SignupSerializer

    def test_subclass(self):
        for c in [PasswordConfirmSerializer, TokenSerializer, serializers.ModelSerializer]:
            with self.subTest():
                self.assertTrue(issubclass(self.serializer, c))

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, User)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 4)
        for field in ['email', 'password', 'password_confirm', 'token']:
            with self.subTest():
                self.assertIn(field, fields)

    def test_password(self):
        field = self.serializer._declared_fields['password']
        self.assertEqual(type(field), PasswordField)

    def test_create(self):
        validated_data = {
            'email': 'u@test.com',
            'password': 'foo123',
            'password_confirm': 'foo123'
        }
        user = self.serializer().create(validated_data)
        self.assertEqual(user.email, validated_data['email'])
        self.assertTrue(user.check_password(validated_data['password']))


class EmailSerializerTests(TestCase):
    def setUp(self):
        self.serializer = EmailSerializer

    def test_subclass(self):
        for c in [CurrentPasswordSerializer, TokenSerializer, serializers.ModelSerializer]:
            with self.subTest():
                self.assertTrue(issubclass(self.serializer, c))

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, User)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 3)
        for field in ['email', 'current_password', 'token']:
            with self.subTest():
                self.assertIn(field, fields)


class PasswordSerializerTests(TestCase):
    def setUp(self):
        self.serializer = PasswordSerializer

    def test_subclass(self):
        for c in [PasswordConfirmSerializer,
                  CurrentPasswordSerializer,
                  serializers.ModelSerializer]:
            with self.subTest():
                self.assertTrue(issubclass(self.serializer, c))

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, User)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 3)
        for field in ['password', 'password_confirm', 'current_password']:
            with self.subTest():
                self.assertIn(field, fields)

    def test_password(self):
        field = self.serializer._declared_fields['password']
        self.assertEqual(type(field), PasswordField)

    def test_update(self):
        user = User.objects.create_user('u@test.com', 'foo123')
        validated_data = {'password': 'bar321'}
        user = self.serializer().update(user, validated_data)
        self.assertTrue(user.check_password(validated_data['password']))


class PasswordResetTokenSerializerTests(TestCase):
    def setUp(self):
        self.serializer = PasswordResetTokenSerializer

    def test_subclass(self):
        self.assertTrue(issubclass(self.serializer, serializers.ModelSerializer))

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, PasswordResetToken)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 1)
        for field in ['email']:
            with self.subTest():
                self.assertIn(field, fields)

    def test_email(self):
        field = self.serializer._declared_fields['email']
        self.assertEqual(type(field), serializers.CharField)
        self.assertTrue(field.write_only)
        self.assertTrue(field.required)

    @patch('project.apps.accounts.serializers.SendGridEmail.send')
    def test_create_created(self, send):
        SendGridEmail.objects.create(title='password-reset')
        user = User.objects.create_user('u@test.com', 'foo123')
        data = {'email': 'u@test.com'}
        token = self.serializer().create(data)
        self.assertEqual(PasswordResetToken.objects.count(), 1)
        self.assertEqual(token.user, user)
        self.assertFalse(token.used)
        send.assert_called_once_with(user.email, data={'token': token.id})

    @patch('project.apps.accounts.serializers.SendGridEmail.send')
    def test_create_not_created(self, send):
        User.objects.create_user('u@test.com', 'foo123')
        data = {'email': 'foo@bar.com'}
        self.serializer().create(data)
        self.assertEqual(PasswordResetToken.objects.count(), 0)
        send.assert_not_called()


class PasswordResetSerializerTests(TestCase):
    def setUp(self):
        self.serializer = PasswordResetSerializer

    def test_subclass(self):
        self.assertTrue(issubclass(self.serializer, PasswordConfirmSerializer))
        self.assertTrue(issubclass(self.serializer, serializers.ModelSerializer))

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, PasswordResetToken)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 2)
        for field in ['password', 'password_confirm']:
            with self.subTest():
                self.assertIn(field, fields)

    def test_password(self):
        field = self.serializer._declared_fields['password']
        self.assertEqual(type(field), PasswordField)
        self.assertTrue(field.required)

    @patch('project.apps.accounts.serializers.PasswordResetToken.is_valid',
           new_callable=PropertyMock(return_value=True))
    def test_validate_valid(self, is_valid):
        token = PasswordResetToken()
        data = {
            'password': 'foo123',
            'password_confirm': 'foo123'
        }
        self.assertEqual(self.serializer(instance=token).validate(data), data)

    @patch('project.apps.accounts.serializers.PasswordResetToken.is_valid',
           new_callable=PropertyMock(return_value=False))
    def test_validate_invalid(self, is_valid):
        token = PasswordResetToken()
        data = {
            'password': 'foo123',
            'password_confirm': 'foo123'
        }
        with self.assertRaises(serializers.ValidationError) as e:
            self.serializer(instance=token).validate(data)
        self.assertEqual(str(e.exception.detail[0]), 'Invalid password reset token.')

    def test_update(self):
        user = User.objects.create_user('u@test.com', 'foo123')
        token = PasswordResetToken.objects.create(user=user)
        data = {'password': 'bar321'}
        self.serializer().update(token, data)
        self.assertTrue(user.check_password(data['password']))
        self.assertTrue(token.used)


class ProfileSerializerTests(TestCase):
    def setUp(self):
        self.serializer = ProfileSerializer

    def test_subclass(self):
        self.assertTrue(self.serializer, serializers.ModelSerializer)

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, User)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 1)
        for field in ['max_followed_progresses']:
            with self.subTest():
                self.assertIn(field, fields)

    def test_read_only_fields(self):
        read_only_fields = self.serializer.Meta.read_only_fields
        self.assertEqual(len(read_only_fields), 1)
        for field in ['max_followed_progresses']:
            with self.subTest():
                self.assertIn(field, read_only_fields)
