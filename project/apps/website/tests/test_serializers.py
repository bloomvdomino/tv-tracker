from django.test import TestCase
from rest_framework import serializers

from ..models import Contact
from ..serializers import ContactSerializer


class ContactSerializerTests(TestCase):
    def setUp(self):
        self.serializer = ContactSerializer

    def test_subclass(self):
        self.assertTrue(issubclass(self.serializer, serializers.ModelSerializer))

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, Contact)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 2)
        for field in ['email', 'message']:
            with self.subTest():
                self.assertIn(field, fields)
