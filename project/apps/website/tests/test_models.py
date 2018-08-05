from django.db import models
from django.test import TestCase

from project.core.models import BaseModel

from ..models import Contact


class ContactModelTests(TestCase):
    def setUp(self):
        self.model = Contact

    def test_subclass(self):
        self.assertTrue(issubclass(self.model, BaseModel))

    def test_ordering(self):
        self.assertEqual(self.model._meta.ordering, ['-created'])

    def test_user(self):
        field = self.model._meta.get_field('email')
        self.assertEqual(type(field), models.EmailField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_message(self):
        field = self.model._meta.get_field('message')
        self.assertEqual(type(field), models.TextField)
        self.assertFalse(field.blank)
