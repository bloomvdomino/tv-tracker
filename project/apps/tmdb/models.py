from django.conf import settings
from django.db import models
from django.utils import timezone

from project.core.models import BaseModel


class Progress(BaseModel):
    RETURNING = 'returning'
    PLANNED = 'planned'
    IN_PRODUCTION = 'in_production'
    ENDED = 'ended'
    CANCELED = 'canceled'
    PILOT = 'pilot'
    SHOW_STATUS_CHOICES = (
        (RETURNING, "Returning Series"),
        (PLANNED, "Planned"),
        (IN_PRODUCTION, "In Production"),
        (ENDED, "Ended"),
        (CANCELED, "Canceled"),
        (PILOT, "Pilot"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name="user")
    is_followed = models.BooleanField(default=False, verbose_name="followed")

    show_id = models.PositiveIntegerField(verbose_name="show ID")
    show_name = models.CharField(max_length=64, verbose_name="show name")
    show_poster_path = models.CharField(max_length=64, blank=True, default='', verbose_name="show poster path")
    show_status = models.CharField(max_length=16, choices=SHOW_STATUS_CHOICES, verbose_name="show status")

    current_season = models.PositiveSmallIntegerField(default=0, verbose_name="current season")
    current_episode = models.PositiveSmallIntegerField(default=0, verbose_name="current episode")
    next_season = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="next season")
    next_episode = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="next episode")
    next_air_date = models.DateField(blank=True, null=True, verbose_name="next air date")

    class Meta:
        unique_together = (('user', 'show_id'),)
        ordering = ['-is_followed', 'next_air_date', 'show_name', 'show_id']
        verbose_name = "progress"
        verbose_name_plural = "progresses"

    @property
    def is_scheduled(self):
        return self.next_air_date is not None

    @property
    def is_available(self):
        return self.is_scheduled and self.next_air_date <= timezone.now().date()

    @property
    def is_finished(self):
        return self.show_status in [self.ENDED, self.CANCELED] and not self.is_scheduled
