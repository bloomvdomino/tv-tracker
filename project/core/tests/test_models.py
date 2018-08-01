import uuid

from django.db import models
from django.test import TestCase

from ..models import BaseModel, BaseUUIDModel


class BaseModelTests(TestCase):
    def setUp(self):
        self.model = BaseModel

    def test_subclass(self):
        self.assertTrue(issubclass(self.model, models.Model))

    def test_abstract(self):
        self.assertTrue(self.model._meta.abstract)

    def test_id(self):
        field = self.model._meta.get_field('id')
        self.assertEqual(type(field), models.BigAutoField)
        self.assertTrue(field.primary_key)
        self.assertFalse(field.editable)

    def test_created(self):
        field = self.model._meta.get_field('created')
        self.assertEqual(type(field), models.DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_updated(self):
        field = self.model._meta.get_field('updated')
        self.assertEqual(type(field), models.DateTimeField)
        self.assertTrue(field.auto_now)


class BaseUUIDModelTests(TestCase):
    def setUp(self):
        self.model = BaseUUIDModel

    def test_subclass(self):
        self.assertTrue(issubclass(self.model, BaseModel))

    def test_abstract(self):
        self.assertTrue(self.model._meta.abstract)

    def test_id(self):
        field = self.model._meta.get_field('id')
        self.assertEqual(type(field), models.UUIDField)
        self.assertTrue(field.primary_key)
        self.assertFalse(field.editable)
        self.assertEqual(field.default, uuid.uuid4)
