from datetime import date

import pytest
from freezegun import freeze_time

from project.apps.accounts.models import User

from ..models import Progress
from .factories import ProgressFactory


class TestProgressModel:
    @pytest.mark.django_db
    @pytest.mark.parametrize('season,episode,not_started', [
        (1, 0, False),
        (0, 1, False),
        (1, 1, False),
        (0, 0, True),
    ])
    def test_not_started(self, season, episode, not_started):
        progress = ProgressFactory.build(current_season=season, current_episode=episode)
        assert progress.not_started is not_started

    @pytest.mark.django_db
    @pytest.mark.parametrize('next_air_date,scheduled', [
        (None, False),
        (date(2019, 3, 16), True),
    ])
    def test_scheduled(self, next_air_date, scheduled):
        progress = ProgressFactory.build(next_air_date=next_air_date)
        assert progress.scheduled is scheduled

    @freeze_time('2018-09-05')
    @pytest.mark.django_db
    @pytest.mark.parametrize('tz, next_air_date,available', [
        (User.TZ_UTC, None, False),
        (User.TZ_UTC, date(2018, 9, 6), False),
        (User.TZ_UTC, date(2018, 9, 5), True),
        (User.TZ_AMERICA_SAO_PAULO, None, False),
        (User.TZ_AMERICA_SAO_PAULO, date(2018, 9, 6), False),
        (User.TZ_AMERICA_SAO_PAULO, date(2018, 9, 5), False),
    ])
    def test_available(self, tz, next_air_date, available):
        progress = ProgressFactory.build(user__time_zone=tz, next_air_date=next_air_date)
        assert progress.available is available

    @pytest.mark.django_db
    @pytest.mark.parametrize('show_status,next_air_date,finished', [
        (Progress.RETURNING, date(2019, 1, 1), False),
        (Progress.PLANNED, date(2019, 1, 1), False),
        (Progress.IN_PRODUCTION, date(2019, 1, 1), False),
        (Progress.ENDED, date(2019, 1, 1), False),
        (Progress.CANCELED, date(2019, 1, 1), False),
        (Progress.PILOT, date(2019, 1, 1), False),
        (Progress.RETURNING, None, False),
        (Progress.PLANNED, None, False),
        (Progress.IN_PRODUCTION, None, False),
        (Progress.ENDED, None, True),
        (Progress.CANCELED, None, True),
        (Progress.PILOT, None, False),
    ])
    def test_finished(self, show_status, next_air_date, finished):
        progress = ProgressFactory.build(show_status=show_status, next_air_date=next_air_date)
        assert progress.finished is finished
