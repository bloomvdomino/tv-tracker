from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from project.apps.emails.models import SendGridEmail

from .jwt import create_token
from .models import PasswordResetToken, User


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update(write_only=True)
        super().__init__(*args, **kwargs)
        self.validators.append(validate_password)


class PasswordConfirmSerializer(serializers.Serializer):
    """
    Validate if the password and the password confirmation are identical.
    """

    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        data = super().validate(data)
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Incorrect password confirmation.")
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
    password = PasswordField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'token')

    def create(self, validated_data):
        validated_data.pop('password_confirm')
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
    password = PasswordField()

    class Meta:
        model = User
        fields = ('password', 'password_confirm', 'current_password')

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class PasswordResetTokenSerializer(serializers.ModelSerializer):
    """
    Used to create a password reset token given a valid email.
    """

    email = serializers.CharField(write_only=True)

    class Meta:
        model = PasswordResetToken
        fields = ('email',)

    def create(self, validated_data):
        instance = self.Meta.model()
        user = User.objects.filter(email=validated_data['email']).first()
        if user:
            instance.user = user
            instance.save()
            sendgrid_email = SendGridEmail.objects.get(title='password-reset')
            sendgrid_email.send(user.email, data={'token': str(instance.id)})
        return instance


class PasswordResetSerializer(PasswordConfirmSerializer,
                              serializers.ModelSerializer):
    """
    Used to reset the password given a valid password reset token.
    """

    password = PasswordField()

    class Meta:
        model = PasswordResetToken
        fields = ('password', 'password_confirm')

    def validate(self, data):
        data = super().validate(data)
        if not self.instance.valid:
            raise serializers.ValidationError("Invalid password reset token.")
        return data

    def update(self, instance, validated_data):
        instance.user.set_password(validated_data['password'])
        instance.user.save()
        instance.used = True
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('max_followed_progresses',)
        read_only_fields = ('max_followed_progresses',)
