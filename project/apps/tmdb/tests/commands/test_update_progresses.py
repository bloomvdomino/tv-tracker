from copy import deepcopy

import pytest
from asynctest import CoroutineMock
from django.conf import settings

from project.apps.tmdb.management.commands.update_progresses import Command


class TestCommand:
    @pytest.fixture
    def command(self):
        return Command()

    def test_fetch_shows(self, mocker, settings, command):
        show_ids = range(1, 4)
        urls = [f"{settings.TMDB_API_URL}tv/{show_id}" for show_id in show_ids]
        responses = [mocker.Mock() for _ in show_ids]
        for show_id in show_ids:
            responses[show_id - 1].json.return_value = {"id": show_id}
        fetch_urls = mocker.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._fetch_urls",
            return_value=responses,
        )

        shows = command._fetch_shows(show_ids)

        assert len(shows) == len(show_ids)
        for show_id in show_ids:
            assert show_id in shows.keys()
        fetch_urls.assert_called_once_with(urls)

    def test_fetch_next_air_dates(self, mocker, command):
        next_air_date = "2019-09-29"

        response = mocker.Mock()
        response.json.return_value = {"air_date": next_air_date}
        fetch_urls = mocker.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._fetch_urls",
            return_value=[response],
        )

        progress_data = {
            1: {"show_id": 11, "next_season": None, "next_episode": None},
            2: {"show_id": 12, "next_season": 2, "next_episode": 3},
            3: {"show_id": 13, "next_season": 3, "next_episode": None},
            4: {"show_id": 14, "next_season": None, "next_episode": 4},
        }
        expected_progress_data = deepcopy(progress_data)
        expected_progress_data[2]["next_air_date"] = next_air_date

        assert command._fetch_next_air_dates(progress_data) == expected_progress_data
        fetch_urls.assert_called_once_with([f"{settings.TMDB_API_URL}tv/12/season/2/episode/3"])

    @pytest.mark.parametrize(
        "url_count,sleep_count", [(1, 0), (2, 0), (3, 0), (4, 1), (5, 1), (6, 1), (7, 2)]
    )
    def test_fetch_urls(self, mocker, settings, command, url_count, sleep_count):
        settings.TMDB_FETCH_CHUNK_SIZE = 3

        sleep = mocker.patch("project.apps.tmdb.management.commands.update_progresses.sleep")
        fetch_url = mocker.patch(
            "project.apps.tmdb.management.commands.update_progresses.Command._fetch_url",
            new=CoroutineMock(),
        )

        responses = command._fetch_urls(["/foo/bar"] * url_count)

        assert len(responses) == url_count
        assert fetch_url.call_count == url_count

        if sleep_count == 0:
            sleep.assert_not_called()
        else:
            assert sleep.call_count == sleep_count
            sleep.assert_called_with(11)

    @pytest.mark.asyncio
    async def test_fetch_url(self, mocker, command):
        response = mocker.Mock()
        client = mocker.Mock()
        client.get = CoroutineMock(return_value=response)
        mocker.patch(
            "project.apps.tmdb.management.commands.update_progresses.httpx.AsyncClient",
            return_value=client,
        )
        url = "/foo/bar"

        r = await command._fetch_url(url)

        assert r == response
        client.get.assert_called_once_with(url, params={"api_key": settings.TMDB_API_KEY})
        response.raise_for_status.assert_called_once_with()
