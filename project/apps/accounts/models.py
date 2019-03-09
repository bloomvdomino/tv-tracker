from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from project.core.models import BaseUUIDModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseUUIDModel):
    email = models.EmailField(unique=True, verbose_name="email")

    is_active = models.BooleanField(default=True, verbose_name="active")
    is_staff = models.BooleanField(default=False, verbose_name="staff")
    is_superuser = models.BooleanField(default=False, verbose_name="superuser")

    max_following_shows = models.PositiveSmallIntegerField(default=8, verbose_name="max following shows")

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-created']
        verbose_name = "user"
        verbose_name_plural = "users"
