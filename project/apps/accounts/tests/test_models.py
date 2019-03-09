from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.test import TestCase

from project.core.models import BaseUUIDModel

from ..managers import UserManager
from ..models import User


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

    def test_max_following_shows(self):
        field = self.model._meta.get_field('max_following_shows')
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
