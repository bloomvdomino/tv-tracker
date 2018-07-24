from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from project.core.models import BaseUUIDModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseUUIDModel):
    email = models.EmailField(unique=True, verbose_name="email")

    max_followed_progresses = models.PositiveSmallIntegerField(
        default=8, verbose_name="max number of followed progresses")

    is_active = models.BooleanField(default=True, verbose_name="active")
    is_staff = models.BooleanField(default=False, verbose_name="staff")
    is_superuser = models.BooleanField(default=False, verbose_name="superuser")

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-created']
        verbose_name = "user"
        verbose_name_plural = "users"
