from datetime import datetime
from unittest.mock import PropertyMock, patch

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.test import TestCase
from django.utils import timezone

from project.apps.tmdb.models import Progress
from project.core.models import BaseUUIDModel

from ..managers import UserManager
from ..models import PasswordResetToken, User


class UserModelTests(TestCase):
    def setUp(self):
        self.model = User

    def test_subclass(self):
        for c in [AbstractBaseUser, PermissionsMixin, BaseUUIDModel]:
            with self.subTest():
                self.assertTrue(issubclass(self.model, c))

    def test_ordering(self):
        self.assertEqual(self.model._meta.ordering, ['-created'])

    def test_objects(self):
        self.assertEqual(self.model.objects, UserManager())

    def test_username_field(self):
        self.assertEqual(self.model.USERNAME_FIELD, 'email')

    def test_email(self):
        field = self.model._meta.get_field('email')
        self.assertEqual(type(field), models.EmailField)
        self.assertTrue(field.unique)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_max_followed_progresses(self):
        field = self.model._meta.get_field('max_followed_progresses')
        self.assertEqual(type(field), models.PositiveSmallIntegerField)
        self.assertEqual(field.default, 8)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_is_active(self):
        field = self.model._meta.get_field('is_active')
        self.assertEqual(type(field), models.BooleanField)
        self.assertTrue(field.default)

    def test_is_staff(self):
        field = self.model._meta.get_field('is_staff')
        self.assertEqual(type(field), models.BooleanField)
        self.assertFalse(field.default)

    def test_is_superuser(self):
        field = self.model._meta.get_field('is_superuser')
        self.assertEqual(type(field), models.BooleanField)
        self.assertFalse(field.default)


class UserModelProgressesTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1@test.com', 'foo123')
        self.u2 = User.objects.create_user('u2@test.com', 'foo123')

        Progress.objects.create(user=self.u1, show_id=1, show_name='Shooter', followed=True)
        Progress.objects.create(user=self.u1, show_id=2, show_name='Impastor', followed=True)

        Progress.objects.create(user=self.u2, show_id=1, show_name='Shooter', followed=True)
        Progress.objects.create(user=self.u2, show_id=2, show_name='Impastor', followed=False)

    def test_added_progresses_count_1(self):
        self.assertEqual(self.u1.added_progresses_count, 2)

    def test_added_progresses_count_2(self):
        self.assertEqual(self.u2.added_progresses_count, 2)

    def test_followed_progresses_count_1(self):
        self.assertEqual(self.u1.followed_progresses_count, 2)

    def test_followed_progresses_count_2(self):
        self.assertEqual(self.u2.followed_progresses_count, 1)


class PasswordResetTokenModelTests(TestCase):
    def setUp(self):
        self.model = PasswordResetToken

    def test_subclass(self):
        self.assertTrue(issubclass(self.model, BaseUUIDModel))

    def test_ordering(self):
        self.assertEqual(self.model._meta.ordering, ['-created'])

    def test_user(self):
        field = self.model._meta.get_field('user')
        self.assertEqual(type(field), models.ForeignKey)
        self.assertEqual(field.remote_field.model, User)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_used(self):
        field = self.model._meta.get_field('used')
        self.assertEqual(type(field), models.BooleanField)
        self.assertFalse(field.default)

    @patch('project.apps.accounts.models.PasswordResetToken.expired', new_callable=PropertyMock(return_value=False))
    def test_valid_true(self, expired):
        self.assertTrue(self.model(used=False).valid)

    @patch('project.apps.accounts.models.PasswordResetToken.expired', new_callable=PropertyMock(return_value=False))
    def test_valid_false_1(self, expired):
        self.assertFalse(self.model(used=True).valid)

    @patch('project.apps.accounts.models.PasswordResetToken.expired', new_callable=PropertyMock(return_value=True))
    def test_valid_false_2(self, expired):
        self.assertFalse(self.model(used=False).valid)

    @patch('project.apps.accounts.models.PasswordResetToken.expired', new_callable=PropertyMock(return_value=True))
    def test_valid_false_3(self, expired):
        self.assertFalse(self.model(used=True).valid)

    @patch('django.utils.timezone.now', return_value=datetime(2018, 8, 4, tzinfo=timezone.utc))
    def test_expired_false(self, now):
        request = self.model(created=datetime(2018, 8, 2, tzinfo=timezone.utc))
        self.assertFalse(request.expired)

    @patch('django.utils.timezone.now', return_value=datetime(2018, 8, 4, tzinfo=timezone.utc))
    def test_expired_true(self, now):
        request = self.model(created=datetime(2018, 8, 1, tzinfo=timezone.utc))
        self.assertTrue(request.expired)
