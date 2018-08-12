from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ..serializers import ContactSerializer
from ..views import ContactView


class ContactViewTests(APITestCase):
    def setUp(self):
        self.view = ContactView

    def test_subclass(self):
        self.assertTrue(issubclass(self.view, generics.CreateAPIView))

    def test_permission_classes(self):
        self.assertEqual(self.view.permission_classes, (AllowAny,))

    def test_serializer_class(self):
        self.assertEqual(self.view.serializer_class, ContactSerializer)
