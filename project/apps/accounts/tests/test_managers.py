from unittest.mock import patch

from django.contrib.auth.models import BaseUserManager
from django.test import TestCase

from ..managers import UserManager
from ..models import User


class UserManagerTests(TestCase):
    def setUp(self):
        self.manager = UserManager

    def test_subclass(self):
        self.assertTrue(issubclass(self.manager, BaseUserManager))

    def test__create_user(self):
        user = User.objects._create_user('u@test.com', '123', is_staff=False, is_superuser=True)
        self.assertEqual(user.email, 'u@test.com')
        self.assertTrue(user.check_password('123'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_superuser)

    @patch('project.apps.accounts.managers.UserManager._create_user')
    def test_create_user(self, _create_user):
        self.manager().create_user('u@test.com', '123', is_staff=True, is_superuser=True, foo=123)
        _create_user.assert_called_once_with('u@test.com', '123', is_staff=False, is_superuser=False, foo=123)

    @patch('project.apps.accounts.managers.UserManager._create_user')
    def test_create_superuser(self, _create_user):
        self.manager().create_superuser('u@test.com', '123', is_staff=False, is_superuser=False, foo=123)
        _create_user.assert_called_once_with('u@test.com', '123', is_staff=True, is_superuser=True, foo=123)
