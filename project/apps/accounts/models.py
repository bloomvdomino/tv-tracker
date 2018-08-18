from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from project.core.models import BaseUUIDModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseUUIDModel):
    email = models.EmailField(unique=True, verbose_name="email")

    max_followed_progresses = models.PositiveSmallIntegerField(
        default=8, verbose_name="max followed progresses")

    is_active = models.BooleanField(default=True, verbose_name="active")
    is_staff = models.BooleanField(default=False, verbose_name="staff")
    is_superuser = models.BooleanField(default=False, verbose_name="superuser")

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-created']
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def added_progresses_count(self):
        return self.progress_set.count()

    @property
    def followed_progresses_count(self):
        return self.progress_set.filter(followed=True).count()


class PasswordResetToken(BaseUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    used = models.BooleanField(default=False, verbose_name="used")

    class Meta:
        ordering = ['-created']
        verbose_name = "password reset token"
        verbose_name_plural = "password reset tokens"

    @property
    def is_valid(self):
        return not (self.used or self.is_expired)

    @property
    def is_expired(self):
        expiration = self.created + timedelta(days=settings.PASSWORD_RESET_TIMEOUT_DAYS)
        return expiration <= timezone.now()
