from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone

from project.apps.tmdb.models import Progress
from project.apps.tmdb.utils import (
    get_air_dates,
    get_next_episode,
    get_shows,
    get_status_value,
)
from project.core.models import BaseUUIDModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseUUIDModel):
    TZ_UTC = 'UTC'
    TZ_AMERICA_NEW_YORK = 'America/New_York'
    TZ_AMERICA_SAO_PAULO = 'America/Sao_Paulo'
    TZ_ASIA_SHANGHAI = 'Asia/Shanghai'
    TZ_CHOICES = (
        (TZ_UTC, "UTC"),
        (TZ_AMERICA_NEW_YORK, "New York"),
        (TZ_AMERICA_SAO_PAULO, "São Paulo"),
        (TZ_ASIA_SHANGHAI, "Shanghai"),
    )

    email = models.EmailField(unique=True, verbose_name="email")
    time_zone = models.CharField(max_length=32, choices=TZ_CHOICES, default=TZ_UTC, verbose_name="time zone")

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

    @property
    def progresses_summary(self):
        """
        Return a summary about the progresses.
        """
        summary = {
            'available': [],
            'scheduled': [],
            'unavailable': [],
            'paused': [],
            'finished': [],
            'stopped': [],
        }
        for progress in self.progress_set.all():
            for key, value in summary.items():
                if getattr(progress, 'list_in_{}'.format(key)):
                    value.append(progress)
                    break
        summary.update(
            saved_count=self.progress_set.count(),
            following_count=self.progress_set.filter(status=Progress.FOLLOWING).count(),
        )
        return summary

    def update_progresses(self):
        """
        Update progresses fields:
            - status
            - show_name
            - show_poster_path
            - show_status
            - next_season
            - next_episode
            - next_air_date
        """
        progresses_data = self._get_updated_progresses_data()
        next_air_dates = self._get_next_air_dates(progresses_data)
        for params in progresses_data:
            for show_id, next_air_date in next_air_dates:
                if params['show_id'] == show_id:
                    params.update(next_air_date=next_air_date)
                    break
            self.progress_set.filter(show_id=params['show_id']).update(**params)
        self._stop_finished_shows()

    def _get_updated_progresses_data(self):
        """
        Return a list of updated data of the progresses which need to be
        updated.
        """
        show_ids = self._get_show_ids_to_update()
        shows = get_shows(show_ids)
        data = []
        for show in shows:
            progress = Progress.objects.get(user=self, show_id=show['id'])
            next_season, next_episode = get_next_episode(
                show,
                progress.current_season,
                progress.current_episode,
            )
            data.append({
                'show_id': show['id'],
                'show_name': show['original_name'],
                'show_poster_path': show['poster_path'],
                'show_status': get_status_value(show['status']),
                'next_season': next_season,
                'next_episode': next_episode,
            })
        return data

    def _get_show_ids_to_update(self):
        """
        Return a list of show IDs of the progresses which need to be updated.
        """
        now = timezone.now()
        last_check_wait = now - timedelta(seconds=settings.TMDB_CHECK_WAIT_SECONDS)
        progresses = self.progress_set.filter(
            Q(last_check__isnull=True) | Q(last_check__lte=last_check_wait),
            ~Q(
                next_season__isnull=False,
                next_episode__isnull=False,
                next_air_date__isnull=False,
            ),
            status=Progress.FOLLOWING,
        )
        show_ids = list(progresses.values_list('show_id', flat=True))
        progresses.update(last_check=now)
        return show_ids

    def _get_next_air_dates(self, progresses):
        """
        Return a tuple (show_id, air_date) of a given list of progresses data,
        which should contain the fields show_id, next_season and next_episode.
        """
        params = [
            {
                'show_id': progress['show_id'],
                'season': progress['next_season'],
                'episode': progress['next_episode'],
            }
            for progress in progresses
            if progress['next_season'] and progress['next_episode']
        ]
        results = get_air_dates(params)
        return [(result['show_id'], result['air_date']) for result in results]

    def _stop_finished_shows(self):
        """
        Update progress status to stopped if the show is finished and the user
        also watched all episodes.
        """
        self.progress_set.filter(
            ~Q(status=Progress.STOPPED),
            show_status__in=[Progress.ENDED, Progress.CANCELED],
            next_air_date__isnull=True,
        ).update(status=Progress.STOPPED)
