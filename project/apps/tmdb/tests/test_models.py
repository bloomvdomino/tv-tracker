from datetime import date

import pytest
from freezegun import freeze_time

from project.apps.accounts.models import User

from ..models import Progress
from .factories import ProgressFactory


class TestProgressModel:
    def test_show(self, mocker):
        show = mocker.MagicMock()
        get_show = mocker.patch("project.apps.tmdb.models.get_show", return_value=show)
        progress = ProgressFactory.build()

        # Should call get_show when accessed by the first time.
        assert progress.show == show
        get_show.assert_called_once_with(progress.show_id)

        # Should not call get_show again as the show should be cached.
        assert progress.show == show
        assert get_show.call_count == 1

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

    def test_delete_url(self):
        progress = ProgressFactory.build()
        assert progress.delete_url == "/show/{}/progress/delete/".format(progress.show_id)

    def test_watch_next_url(self):
        progress = ProgressFactory.build()
        assert progress.watch_next_url == "/progress/watch_next/{}/".format(progress.show_id)

    def test_last_aired_label_none(self):
        progress = ProgressFactory.build()
        assert progress.last_aired_label is None

    def test_last_aired_label(self):
        progress = ProgressFactory.build(last_aired_season=3, last_aired_episode=5)
        assert progress.last_aired_label == "S03E05"

    @pytest.mark.django_db
    def test_update_show_data(self, mocker):
        show = mocker.MagicMock()
        type(show).name = mocker.PropertyMock(return_value="Foo")
        type(show).poster_path = mocker.PropertyMock(return_value="/foo.jpg")
        type(show).status_value = mocker.PropertyMock(return_value="ended")
        type(show).last_aired_episode = mocker.PropertyMock(return_value=(15, 11))

        get_show = mocker.patch("project.apps.tmdb.models.get_show", return_value=show)

        progress = ProgressFactory()
        progress.update_show_data()
        progress.refresh_from_db()

        get_show.assert_called_once_with(progress.show_id)
        assert progress.show_name == show.name
        assert progress.show_poster_path == show.poster_path
        assert progress.show_status == show.status_value
        assert progress.last_aired_season == show.last_aired_episode[0]
        assert progress.last_aired_episode == show.last_aired_episode[1]

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
        save.assert_called_once_with(
            update_fields=[
                "current_season",
                "current_episode",
                "next_season",
                "next_episode",
                "next_air_date",
            ]
        )

    def test_update_episodes(self, mocker):
        show = mocker.MagicMock()
        show.get_next_episode.return_value = (1, 2)
        mocker.patch("project.apps.tmdb.models.get_show", return_value=show)
        progress = ProgressFactory.build()

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
