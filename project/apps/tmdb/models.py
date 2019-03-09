from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from project.core.models import BaseModel

from .utils import format_episode_label


class Progress(BaseModel):
    FOLLOWING = 'following'
    PAUSED = 'paused'
    STOPPED = 'stopped'
    STATUS_CHOICES = (
        (FOLLOWING, "Following"),
        (PAUSED, "Paused"),
        (STOPPED, "Stopped"),
    )

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
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=FOLLOWING, verbose_name="status")

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
    def not_started(self):
        return self.current_season == 0 and self.current_episode == 0

    @property
    def is_scheduled(self):
        return self.next_air_date is not None

    @property
    def is_available(self):
        return self.is_scheduled and self.next_air_date <= timezone.now().date()

    @property
    def is_finished(self):
        return self.show_status in [self.ENDED, self.CANCELED] and not self.is_scheduled

    @property
    def list_in_available(self):
        return self.status == self.FOLLOWING and self.is_available

    @property
    def list_in_scheduled(self):
        return self.status == self.FOLLOWING and not self.is_available and self.is_scheduled

    @property
    def list_in_unavailable(self):
        return (
            not self.is_finished and
            self.status == self.FOLLOWING and
            not (self.list_in_available or self.list_in_scheduled)
        )

    @property
    def list_in_paused(self):
        return not self.is_finished and self.status == self.PAUSED

    @property
    def list_in_stopped(self):
        return not self.is_finished and self.status == self.STOPPED

    @property
    def list_in_finished(self):
        return self.is_finished

    @property
    def detail_url(self):
        return reverse('tmdb:show', kwargs={'id': self.show_id})

    @property
    def last_watched_label(self):
        return format_episode_label(self.current_season, self.current_episode)

    @property
    def next_to_watch_label(self):
        if not (self.next_season and self.next_episode):
            return None
        return format_episode_label(self.next_season, self.next_episode)
