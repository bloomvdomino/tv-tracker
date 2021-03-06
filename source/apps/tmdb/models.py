from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

from source.apps.tmdb.utils import format_episode_label, get_air_date, get_show
from source.core.models import BaseModel


class Progress(BaseModel):
    # Progress status.
    FOLLOWING = "following"
    PAUSED = "paused"
    STOPPED = "stopped"
    STATUS_CHOICES = ((FOLLOWING, "Following"), (PAUSED, "Paused"), (STOPPED, "Stopped"))

    # Show status.
    RETURNING = "returning"
    PLANNED = "planned"
    IN_PRODUCTION = "in_production"
    ENDED = "ended"
    CANCELED = "canceled"
    PILOT = "pilot"
    SHOW_STATUS_CHOICES = (
        (RETURNING, "Returning Series"),
        (PLANNED, "Planned"),
        (IN_PRODUCTION, "In Production"),
        (ENDED, "Ended"),
        (CANCELED, "Canceled"),
        (PILOT, "Pilot"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name="user")
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=FOLLOWING, verbose_name="status"
    )

    show_id = models.PositiveIntegerField(verbose_name="show ID")
    show_name = models.CharField(max_length=64, verbose_name="show name")
    show_poster_path = models.CharField(
        max_length=64, blank=True, default="", verbose_name="show poster path"
    )
    show_status = models.CharField(
        max_length=16, choices=SHOW_STATUS_CHOICES, verbose_name="show status"
    )
    show_genres = ArrayField(
        models.CharField(max_length=32), default=list, verbose_name="show genres"
    )
    show_languages = ArrayField(
        models.CharField(max_length=8), default=list, verbose_name="show languages"
    )

    current_season = models.PositiveSmallIntegerField(default=0, verbose_name="current season")
    current_episode = models.PositiveSmallIntegerField(default=0, verbose_name="current episode")
    next_season = models.PositiveSmallIntegerField(
        blank=True, null=True, default=1, verbose_name="next season"
    )
    next_episode = models.PositiveSmallIntegerField(
        blank=True, null=True, default=1, verbose_name="next episode"
    )
    next_air_date = models.DateField(blank=True, null=True, verbose_name="next air date")
    last_aired_season = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="last aired season"
    )
    last_aired_episode = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="last aired episode"
    )

    class Meta:
        unique_together = (("user", "show_id"),)
        ordering = ["next_air_date", "show_name", "show_id"]
        verbose_name = "progress"
        verbose_name_plural = "progresses"

    @cached_property
    def show(self):
        return get_show(self.show_id)

    @property
    def not_started(self):
        return self.current_season == 0 and self.current_episode == 0

    @property
    def scheduled(self):
        return self.next_air_date is not None

    @property
    def available(self):
        if not self.scheduled:
            return False

        tz = timezone.pytz.timezone(self.user.time_zone)
        today = timezone.localdate(timezone=tz)
        return self.next_air_date <= today

    @property
    def finished(self):
        return self.show_status in [self.ENDED, self.CANCELED] and not self.scheduled

    @property
    def list_in_available(self):
        return self.status == self.FOLLOWING and self.available

    @property
    def list_in_scheduled(self):
        return self.status == self.FOLLOWING and not self.available and self.scheduled

    @property
    def list_in_unavailable(self):
        return (
            not self.finished
            and self.status == self.FOLLOWING
            and not (self.list_in_available or self.list_in_scheduled)
        )

    @property
    def list_in_paused(self):
        return not self.finished and self.status == self.PAUSED

    @property
    def list_in_stopped(self):
        return not self.finished and self.status == self.STOPPED

    @property
    def list_in_finished(self):
        return self.finished

    @property
    def update_url(self):
        return reverse("tmdb:progress_update", kwargs={"show_id": self.show_id})

    @property
    def delete_url(self):
        return reverse("tmdb:progress_delete", kwargs={"show_id": self.show_id})

    @property
    def watch_next_url(self):
        return reverse("tmdb:watch_next", kwargs={"show_id": self.show_id})

    @property
    def last_watched_label(self):
        return format_episode_label(self.current_season, self.current_episode)

    @property
    def next_to_watch_label(self):
        if not (self.next_season and self.next_episode):
            return None
        return format_episode_label(self.next_season, self.next_episode)

    @property
    def last_aired_label(self):
        if not (self.last_aired_season and self.last_aired_episode):
            return None
        return format_episode_label(self.last_aired_season, self.last_aired_episode)

    def update_show_data(self):
        self.show_name = self.show.name
        self.show_poster_path = self.show.poster_path
        self.show_status = self.show.status_value
        self.show_genres = self.show.genres
        self.show_languages = self.show.languages
        self.last_aired_season, self.last_aired_episode = self.show.last_aired_episode

    def watch_next(self):
        self.current_season, self.current_episode = self.next_season, self.next_episode
        self.next_season, self.next_episode = self.show.get_next_episode(
            self.current_season, self.current_episode
        )
        self.update_next_air_date()

    def update_next_air_date(self):
        if self.next_season and self.next_episode:
            self.next_air_date = get_air_date(self.show_id, self.next_season, self.next_episode)
        else:
            self.next_air_date = None

    def stop_if_finished(self):
        if (
            self.status != self.STOPPED
            and self.show_status in [self.ENDED, self.CANCELED]
            and self.next_air_date is None
        ):
            self.status = self.STOPPED
