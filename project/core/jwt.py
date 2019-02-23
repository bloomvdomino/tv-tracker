from calendar import timegm
from datetime import datetime

from rest_framework_jwt.settings import api_settings


def payload_handler(user):
    payload = {
        'email': user.email,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
    }

    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def payload_username_handler(payload):
    return payload.get('email')


def create_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token
