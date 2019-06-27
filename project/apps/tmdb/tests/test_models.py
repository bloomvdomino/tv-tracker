from datetime import date

import pytest
from freezegun import freeze_time

from project.apps.accounts.models import User

from ..models import Progress
from .factories import ProgressFactory


class TestProgressModel:
    def test_init(self):
        progress = ProgressFactory.build()
        assert progress._show is None

    def test_show_fetched(self, mocker):
        show = mocker.MagicMock()
        get_show = mocker.patch("project.apps.tmdb.models.get_show", return_value=show)
        progress = ProgressFactory.build()

        assert progress.show == show
        get_show.assert_called_once_with(progress.show_id)

    def test_show_cached(self, mocker):
        get_show = mocker.patch("project.apps.tmdb.models.get_show")
        show = mocker.MagicMock()
        progress = ProgressFactory.build()
        progress._show = show

        assert progress.show == show
        get_show.assert_not_called()

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "season,episode,not_started", [(1, 0, False), (0, 1, False), (1, 1, False), (0, 0, True)]
    )
    def test_not_started(self, season, episode, not_started):
        progress = ProgressFactory.build(current_season=season, current_episode=episode)
        assert progress.not_started is not_started

    @pytest.mark.django_db
    @pytest.mark.parametrize("next_air_date,scheduled", [(None, False), (date(2019, 3, 16), True)])
    def test_scheduled(self, next_air_date, scheduled):
        progress = ProgressFactory.build(next_air_date=next_air_date)
        assert progress.scheduled is scheduled

    @freeze_time("2018-09-05")
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "tz, next_air_date,available",
        [
            (User.TZ_UTC, None, False),
            (User.TZ_UTC, date(2018, 9, 6), False),
            (User.TZ_UTC, date(2018, 9, 5), True),
            (User.TZ_AMERICA_SAO_PAULO, None, False),
            (User.TZ_AMERICA_SAO_PAULO, date(2018, 9, 6), False),
            (User.TZ_AMERICA_SAO_PAULO, date(2018, 9, 5), False),
        ],
    )
    def test_available(self, tz, next_air_date, available):
        progress = ProgressFactory.build(user__time_zone=tz, next_air_date=next_air_date)
        assert progress.available is available

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "show_status,next_air_date,finished",
        [
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
        ],
    )
    def test_finished(self, show_status, next_air_date, finished):
        progress = ProgressFactory.build(show_status=show_status, next_air_date=next_air_date)
        assert progress.finished is finished

    def test_update_url(self):
        progress = ProgressFactory.build()
        assert progress.update_url == "/show/{}/progress/update/".format(progress.show_id)

    def test_watch_next_url(self):
        progress = ProgressFactory.build()
        assert progress.watch_next_url == "/progress/watch_next/{}/".format(progress.show_id)

    def test_last_aired_label_none(self):
        progress = ProgressFactory.build()
        assert progress.last_aired_label is None

    def test_last_aired_label(self):
        progress = ProgressFactory.build(last_aired_season=3, last_aired_episode=5)
        assert progress.last_aired_label == "S03E05"

    def test_watch_next(self, mocker):
        update_episodes = mocker.patch("project.apps.tmdb.models.Progress._update_episodes")
        update_next_air_date = mocker.patch(
            "project.apps.tmdb.models.Progress.update_next_air_date"
        )
        save = mocker.patch("project.apps.tmdb.models.Progress.save")

        progress = ProgressFactory.build()
        progress.watch_next()

        update_episodes.assert_called_once_with()
        update_next_air_date.assert_called_once_with()
        save.assert_called_once_with()

    def test_update_episodes(self, mocker):
        show = mocker.MagicMock()
        show.get_next_episode.return_value = (1, 2)
        progress = ProgressFactory.build()
        progress._show = show

        progress._update_episodes()

        assert progress.current_season == 1
        assert progress.current_episode == 1
        assert progress.next_season == 1
        assert progress.next_episode == 2

        show.get_next_episode.assert_called_once_with(1, 1)

    def test_update_next_air_date(self, mocker):
        get_air_date = mocker.patch(
            "project.apps.tmdb.models.get_air_date", return_value=date(2019, 6, 22)
        )
        progress = ProgressFactory.build()

        progress.update_next_air_date()

        assert progress.next_air_date == date(2019, 6, 22)
        get_air_date.assert_called_once_with(progress.show_id, 1, 1)

    @pytest.mark.parametrize("next_season,next_episode", [(None, None), (2, None), (None, 2)])
    def test_update_next_air_date_none(self, mocker, next_season, next_episode):
        get_air_date = mocker.patch("project.apps.tmdb.models.get_air_date")
        progress = ProgressFactory.build(next_season=next_season, next_episode=next_episode)

        progress.update_next_air_date()

        assert progress.next_air_date is None
        get_air_date.assert_not_called()

    def test_update_last_aired_episode(self, mocker):
        show = mocker.MagicMock()
        type(show).last_aired_episode = mocker.PropertyMock(return_value=(2, 3))
        progress = ProgressFactory.build()
        progress._show = show

        progress.update_last_aired_episode()

        assert progress.last_aired_season == 2
        assert progress.last_aired_episode == 3
