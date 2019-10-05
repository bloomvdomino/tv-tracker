from datetime import date

import asynctest
import pytest
from django.conf import settings

from project.apps.tmdb.management.commands.update_progresses import Command
from project.apps.tmdb.models import Progress
from project.apps.tmdb.tests.factories import ProgressFactory


class TestCommand:
    @pytest.fixture
    def command(self):
        return Command()

    @pytest.mark.asyncio
    async def test_update_progress_skipped(self, command):
        progress = ProgressFactory.build()

        with asynctest.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._get_show",
            return_value=None,
        ) as get_show:
            with asynctest.patch(
                "project.apps.tmdb.management.commands.update_progresses.Command._get_next"
            ) as get_next:
                await command._update_progress(progress)

        get_show.assert_awaited_once_with(progress.show_id)
        get_next.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.django_db
    async def test_update_progress(self, mocker, command):
        progress = ProgressFactory()

        show = mocker.MagicMock(
            poster_path="/foo.jpg", status_value=Progress.ENDED, last_aired_episode=(4, 5)
        )
        show.name = "Foo"

        stop_if_finished = mocker.patch("project.apps.tmdb.models.Progress.stop_if_finished")

        with asynctest.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._get_show",
            return_value=show,
        ) as get_show:
            with asynctest.patch(
                "project.apps.tmdb.management.commands.update_progresses.Command._get_next",
                return_value=(3, 2, "2019-10-05"),
            ) as get_next:
                await command._update_progress(progress)

        get_show.assert_awaited_once_with(progress.show_id)
        get_next.assert_awaited_once_with(show, progress.current_season, progress.current_episode)

        progress.refresh_from_db()

        assert progress.show_name == show.name
        assert progress.show_poster_path == show.poster_path
        assert progress.show_status == show.status_value
        assert progress.next_season == 3
        assert progress.next_episode == 2
        assert progress.next_air_date == date(2019, 10, 5)
        assert progress.last_aired_season == show.last_aired_episode[0]
        assert progress.last_aired_episode == show.last_aired_episode[1]

        stop_if_finished.assert_called_once_with()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", [200, 404])
    async def test_get_show(self, mocker, command, status_code):
        show_id = 123

        response = mocker.MagicMock(status_code=status_code)
        response.json.return_value = {"id": show_id}

        with asynctest.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._fetch",
            return_value=response,
        ) as fetch:
            show = await command._get_show(show_id)

        fetch.assert_awaited_once_with(f"{settings.TMDB_API_URL}tv/{show_id}")

        if status_code == 200:
            assert show.id == show_id
        else:
            assert show is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "returned,expected",
        [
            ((2, 4), (2, 4, "2019-10-05")),
            ((2, None), (None, None, None)),
            ((None, 3), (None, None, None)),
            ((None, None), (None, None, None)),
        ],
    )
    async def test_get_next(self, mocker, command, returned, expected):
        show = mocker.MagicMock(id=1)
        show.get_next_episode.return_value = returned

        with asynctest.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._get_air_date",
            return_value=expected[2],
        ) as get_air_date:
            assert await command._get_next(show, 2, 3) == expected

        show.get_next_episode.assert_called_once_with(2, 3)

        if all(returned):
            get_air_date.assert_awaited_once_with(1, expected[0], expected[1])
        else:
            get_air_date.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status_code,data,air_date",
        [
            (200, {"air_date": "2019-10-05"}, "2019-10-05"),
            (200, {"air_date": ""}, None),
            (200, {}, None),
            (404, {"air_date": ""}, None),
            (404, {}, None),
        ],
    )
    async def test_get_air_date(self, command, mocker, status_code, data, air_date):
        response = mocker.MagicMock(status_code=status_code)
        response.json.return_value = data

        with asynctest.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._fetch",
            return_value=response,
        ) as fetch:
            assert await command._get_air_date(1, 2, 3) == air_date

        fetch.assert_awaited_once_with(f"{settings.TMDB_API_URL}tv/1/season/2/episode/3")

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", [200, 404, 429, 500])
    async def test_fetch(self, mocker, command, status_code):
        response = mocker.MagicMock(status_code=status_code)

        client = asynctest.MagicMock()
        client.get = asynctest.CoroutineMock(return_value=response)

        url = "/foo/bar"

        with asynctest.patch(
            "project.apps.tmdb.management.commands.update_progresses.httpx.AsyncClient"
        ) as async_client:
            async_client.return_value.__aenter__.return_value = client
            r = await command._fetch(url)

        assert r == response
        client.get.assert_awaited_once_with(url, params={"api_key": settings.TMDB_API_KEY})

        if status_code == 404:
            response.raise_for_status.assert_not_called()
        else:
            response.raise_for_status.assert_called_once_with()
