from django.test import TestCase
from rest_framework_jwt.settings import api_settings

from project.apps.accounts.models import User

from ..jwt import create_token, payload_handler, payload_username_handler


class JWTTests(TestCase):
    def setUp(self):
        api_settings.JWT_ALLOW_REFRESH = True
        api_settings.JWT_AUDIENCE = 'JWT_AUDIENCE'
        api_settings.JWT_ISSUER = 'JWT_ISSUER'
        self.user = User(email='u@test.com')

    def test_payload_handler(self):
        payload = payload_handler(self.user)
        self.assertPayload(payload)

    def test_payload_username_handler(self):
        username = payload_username_handler({'email': self.user.email})
        self.assertEqual(username, self.user.email)

    def test_create_token(self):
        encoded = create_token(self.user)
        decoded = api_settings.JWT_DECODE_HANDLER(encoded)
        self.assertPayload(decoded)

    def assertPayload(self, payload):
        self.assertEqual(payload['email'], self.user.email)
        self.assertIn('exp', payload)
        self.assertIn('orig_iat', payload)
        self.assertEqual(payload['aud'], api_settings.JWT_AUDIENCE)
        self.assertEqual(payload['iss'], api_settings.JWT_ISSUER)
