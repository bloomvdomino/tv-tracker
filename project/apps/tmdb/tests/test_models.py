from django.db import models
from django.test import TestCase

from project.apps.accounts.models import User
from project.core.models import BaseModel

from ..models import Progress


class ProgressModelTests(TestCase):
    def setUp(self):
        self.model = Progress

    def test_subclass(self):
        self.assertTrue(issubclass(self.model, BaseModel))

    def test_unique_together(self):
        self.assertEqual(self.model._meta.unique_together, (('user', 'show_id'),))

    def test_ordering(self):
        self.assertEqual(
            self.model._meta.ordering, ['-followed', 'next_air_date', 'show_name', 'show_id'])

    def test_show_status_choices(self):
        self.assertEqual(self.model.RETURNING, 'returning')
        self.assertEqual(self.model.PLANNED, 'planned')
        self.assertEqual(self.model.IN_PRODUCTION, 'in_production')
        self.assertEqual(self.model.ENDED, 'ended')
        self.assertEqual(self.model.CANCELED, 'canceled')
        self.assertEqual(self.model.PILOT, 'pilot')
        self.assertEqual(self.model.SHOW_STATUS_CHOICES, (
            ('returning', 'Returning Series'),
            ('planned', 'Planned'),
            ('in_production', 'In Production'),
            ('ended', 'Ended'),
            ('canceled', 'Canceled'),
            ('pilot', 'Pilot')
        ))

    def test_user(self):
        field = self.model._meta.get_field('user')
        self.assertEqual(type(field), models.ForeignKey)
        self.assertEqual(field.remote_field.model, User)
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_followed(self):
        field = self.model._meta.get_field('followed')
        self.assertEqual(type(field), models.BooleanField)
        self.assertFalse(field.default)

    def test_show_id(self):
        field = self.model._meta.get_field('show_id')
        self.assertEqual(type(field), models.PositiveIntegerField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_show_name(self):
        field = self.model._meta.get_field('show_name')
        self.assertEqual(type(field), models.CharField)
        self.assertEqual(field.max_length, 64)
        self.assertFalse(field.blank)

    def test_show_poster_path(self):
        field = self.model._meta.get_field('show_poster_path')
        self.assertEqual(type(field), models.CharField)
        self.assertEqual(field.max_length, 64)
        self.assertTrue(field.blank)
        self.assertEqual(field.default, '')

    def test_show_status(self):
        field = self.model._meta.get_field('show_status')
        self.assertEqual(type(field), models.CharField)
        self.assertEqual(field.max_length, 16)
        self.assertFalse(field.blank)
        self.assertEqual(field.choices, self.model.SHOW_STATUS_CHOICES)

    def test_current_season(self):
        field = self.model._meta.get_field('current_season')
        self.assertEqual(type(field), models.PositiveSmallIntegerField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)
        self.assertEqual(field.default, 0)

    def test_current_episode(self):
        field = self.model._meta.get_field('current_episode')
        self.assertEqual(type(field), models.PositiveSmallIntegerField)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)
        self.assertEqual(field.default, 0)

    def test_next_season(self):
        field = self.model._meta.get_field('next_season')
        self.assertEqual(type(field), models.PositiveSmallIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)
        self.assertEqual(field.default, 1)

    def test_next_episode(self):
        field = self.model._meta.get_field('next_episode')
        self.assertEqual(type(field), models.PositiveSmallIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)
        self.assertEqual(field.default, 1)

    def test_next_air_date(self):
        field = self.model._meta.get_field('next_air_date')
        self.assertEqual(type(field), models.DateField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)
