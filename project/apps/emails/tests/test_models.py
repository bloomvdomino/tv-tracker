from unittest.mock import patch

from django.db import models
from django.test import TestCase, override_settings

from project.core.models import BaseModel

from ..models import SendGridEmail


class SendGridEmailModelTests(TestCase):
    def setUp(self):
        self.model = SendGridEmail

    def test_subclass(self):
        self.assertTrue(issubclass(self.model, BaseModel))

    def test_ordering(self):
        self.assertEqual(self.model._meta.ordering, ['title'])

    def test_title(self):
        field = self.model._meta.get_field('title')
        self.assertEqual(type(field), models.CharField)
        self.assertEqual(field.max_length, 32)
        self.assertTrue(field.unique)
        self.assertFalse(field.blank)

    def test_template_id(self):
        field = self.model._meta.get_field('template_id')
        self.assertEqual(type(field), models.CharField)
        self.assertEqual(field.max_length, 64)
        self.assertFalse(field.blank)

    @override_settings(SENDGRID_SANDBOX_MODE=True)
    def test_sandbox_mode_enabled(self):
        mail_settings = self.model()._build_mail_settings()
        self.assertTrue(mail_settings.sandbox_mode.enable)

    @override_settings(SENDGRID_SANDBOX_MODE=False)
    def test_sandbox_mode_disabled(self):
        mail_settings = self.model()._build_mail_settings()
        self.assertFalse(mail_settings.sandbox_mode.enable)


@patch('project.apps.emails.models.sendgrid.SendGridAPIClient')
@patch('project.apps.emails.models.SendGridEmail._build_mail_settings')
class SendGridEmailModelSendTests(TestCase):
    def setUp(self):
        self.to_email = 'to@email.com'
        self.data = {'foo', 'bar'}
        self.mail = SendGridEmail(template_id='template_id')

    def test_exception(self, _build_mail_settings, SendGridAPIClient):
        SendGridAPIClient.return_value.client.mail.send.post.side_effect = Exception()
        with self.assertRaises(Exception):
            self.mail.send(self.to_email, data=self.data)
        _build_mail_settings.assert_called_once_with()

    def test_unexpected_status_code(self, _build_mail_settings, SendGridAPIClient):
        SendGridAPIClient.return_value.client.mail.send.post.return_value.status_code = 400
        with self.assertRaises(Exception):
            self.mail.send(self.to_email, data=self.data)
        _build_mail_settings.assert_called_once_with()

    def test_success(self, _build_mail_settings, SendGridAPIClient):
        SendGridAPIClient.return_value.client.mail.send.post.return_value.status_code = 202
        self.mail.send(self.to_email, data=self.data)
        _build_mail_settings.assert_called_once_with()
        SendGridAPIClient.return_value.client.mail.send.post.assert_called_once()
