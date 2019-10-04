from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Q

from project.apps.accounts.managers import UserManager
from project.apps.tmdb.models import Progress
from project.core.models import BaseUUIDModel


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

    @property
    def progresses_summary(self):
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
        for progress in self.progress_set.all():
            for key, value in summary.items():
                if getattr(progress, "list_in_{}".format(key)):
                    value.append(progress)
                    break
        summary.update(
            saved_count=self.progress_set.count(),
            following_count=self.progress_set.filter(status=Progress.FOLLOWING).count(),
        )
        return summary

    def stop_finished_shows(self):
        """
        Update progress status to stopped if the show is finished and the user
        also watched all episodes.
        """
        self.progress_set.filter(
            ~Q(status=Progress.STOPPED),
            show_status__in=[Progress.ENDED, Progress.CANCELED],
            next_air_date__isnull=True,
        ).update(status=Progress.STOPPED)
