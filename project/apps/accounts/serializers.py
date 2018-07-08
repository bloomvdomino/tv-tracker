from django.contrib.auth import password_validation
from rest_framework import serializers

from .jwt import create_token
from .models import User


class PasswordConfirmSerializer(serializers.Serializer):
    """
    Validate if the password and the password confirmation are identical.
    """

    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        data = super().validate(data)
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Incorrect password confirmation.")
        del data['password_confirm']
        return data


class CurrentPasswordSerializer(serializers.Serializer):
    """
    Validate the current password of the user.
    """

    current_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError("Incorrect current password.")
        return value

    def validate(self, data):
        data = super().validate(data)
        del data['current_password']
        return data


class TokenSerializer(serializers.Serializer):
    """
    Return a new token for the user.
    """

    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        return create_token(obj)


class SignupSerializer(PasswordConfirmSerializer,
                       TokenSerializer,
                       serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'token')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        password_validation.validate_password(password=value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailSerializer(CurrentPasswordSerializer,
                      TokenSerializer,
                      serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'current_password', 'token')


class PasswordSerializer(PasswordConfirmSerializer,
                         CurrentPasswordSerializer,
                         serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'password_confirm', 'current_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        password_validation.validate_password(password=value)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
