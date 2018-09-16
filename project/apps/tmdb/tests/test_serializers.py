from django.test import TestCase
from rest_framework import serializers

from ..models import Progress
from ..serializers import ProgressSerializer


class ProgressSerializerTests(TestCase):
    def setUp(self):
        self.serializer = ProgressSerializer

    def test_subclass(self):
        self.assertTrue(issubclass(self.serializer, serializers.ModelSerializer))

    def test_model(self):
        self.assertEqual(self.serializer.Meta.model, Progress)

    def test_fields(self):
        fields = self.serializer.Meta.fields
        self.assertEqual(len(fields), 16)
        for field in ['user', 'show_id', 'show_name', 'show_poster_path', 'show_status', 'show_status_text',
                      'current_season', 'current_episode', 'next_season', 'next_episode', 'next_air_date',
                      'updated', 'is_followed', 'is_scheduled', 'is_available', 'is_finished']:
            with self.subTest():
                self.assertIn(field, fields)

    def test_user(self):
        field = self.serializer._declared_fields.get('user')
        self.assertEqual(type(field), serializers.HiddenField)
        self.assertEqual(type(field.default), serializers.CurrentUserDefault)

    def test_show_status_text(self):
        field = self.serializer._declared_fields.get('show_status_text')
        self.assertEqual(type(field), serializers.SerializerMethodField)

    def test_get_show_status_text(self):
        progress = Progress(show_status=Progress.RETURNING)
        self.assertEqual(self.serializer().get_show_status_text(progress), 'Returning Series')
