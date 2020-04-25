from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from source.apps.accounts.managers import UserManager
from source.apps.tmdb.models import Progress
from source.core.models import BaseUUIDModel


class User(AbstractBaseUser, PermissionsMixin, BaseUUIDModel):
    TZ_UTC = "UTC"
    TZ_AMERICA_NEW_YORK = "America/New_York"
    TZ_AMERICA_SAO_PAULO = "America/Sao_Paulo"
    TZ_ASIA_SHANGHAI = "Asia/Shanghai"
    TZ_CHOICES = (
        (TZ_UTC, "UTC"),
        (TZ_AMERICA_NEW_YORK, "New York"),
        (TZ_AMERICA_SAO_PAULO, "São Paulo"),
        (TZ_ASIA_SHANGHAI, "Shanghai"),
    )

    email = models.EmailField(unique=True, verbose_name="email")
    time_zone = models.CharField(
        max_length=32, choices=TZ_CHOICES, default=TZ_UTC, verbose_name="time zone"
    )

    is_active = models.BooleanField(default=True, verbose_name="active")
    is_staff = models.BooleanField(default=False, verbose_name="staff")
    is_superuser = models.BooleanField(default=False, verbose_name="superuser")

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["-created"]
        verbose_name = "user"
        verbose_name_plural = "users"

    def progresses_summary(self, genre=None, language=None):
        """
        Return a summary about the progresses.
        """
        summary = {
            "available": [],
            "scheduled": [],
            "unavailable": [],
            "paused": [],
            "finished": [],
            "stopped": [],
        }
        progresses = self.progress_set.all()
        if genre:
            progresses = progresses.filter(show_genres__contains=[genre])
        if language:
            progresses = progresses.filter(show_languages__contains=[language])
        for progress in progresses:
            for key, value in summary.items():
                if getattr(progress, f"list_in_{key}"):
                    value.append(progress)
                    break
        summary.update(
            saved_count=progresses.count(),
            following_count=progresses.filter(status=Progress.FOLLOWING).count(),
        )
        return summary
