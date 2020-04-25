from unittest.mock import AsyncMock

import httpx
import pytest
from django.conf import settings

from source.apps.tmdb.management.commands.update_progresses import Command
from source.apps.tmdb.models import Progress
from source.apps.tmdb.tests.factories import ProgressFactory


class TestCommand:
    @pytest.fixture
    def command(self):
        return Command()

    @property
    def mock_path(self):
        return "source.apps.tmdb.management.commands.update_progresses"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("total,chunk_size,chunk_len", [(2, 3, 1), (3, 3, 1), (4, 3, 2)])
    async def test_get_progress_chunks(self, mocker, command, total, chunk_size, chunk_len):
        progresses = [ProgressFactory.build() for _ in range(total)]
        mocker.patch(f"{self.mock_path}.Progress.objects.all", return_value=progresses)

        chunks = await command._get_progress_chunks(chunk_size)

        assert len(chunks) == chunk_len

    def test_capture_exceptions_without_error(self, mocker, command):
        capture_exception = mocker.patch(f"{self.mock_path}.capture_exception")
        command._capture_exceptions([1, 3, 2])
        capture_exception.assert_not_called()

    def test_capture_exceptions_with_error(self, mocker, command):
        capture_exception = mocker.patch(f"{self.mock_path}.capture_exception")
        results = [1, Exception(), 2]

        command._capture_exceptions(results)

        capture_exception.assert_called_once_with(results[1])

    def test_capture_exceptions_with_errors(self, mocker, command):
        capture_exception = mocker.patch(f"{self.mock_path}.capture_exception")
        results = [1, Exception(), 2, Exception()]

        command._capture_exceptions(results)

        assert capture_exception.call_count == 2
        capture_exception.assert_any_call(results[1])
        capture_exception.assert_any_call(results[3])

    @pytest.mark.asyncio
    async def test_update_progress_skipped(self, mocker, command):
        progress = ProgressFactory.build()

        get_show = mocker.patch(f"{self.mock_path}.Command._get_show", return_value=None)
        get_next = mocker.patch(f"{self.mock_path}.Command._get_next")

        await command._update_progress(progress)

        get_show.assert_awaited_once_with(progress.show_id)
        get_next.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_progress(self, mocker, command):
        progress = ProgressFactory.build()

        show = mocker.MagicMock(
            poster_path="/foo.jpg",
            status_value=Progress.ENDED,
            genres=["Action"],
            languages=["en"],
            last_aired_episode=(4, 5),
        )
        show.name = "Foo"

        stop_if_finished = mocker.patch("source.apps.tmdb.models.Progress.stop_if_finished")

        patch_path = f"{self.mock_path}.Command"
        get_show = mocker.patch(f"{patch_path}._get_show", return_value=show)
        get_next = mocker.patch(f"{patch_path}._get_next", return_value=(3, 2, "2019-10-05"))
        save_progress = mocker.patch(f"{patch_path}._save_progress")

        await command._update_progress(progress)

        get_show.assert_awaited_once_with(progress.show_id)
        get_next.assert_awaited_once_with(show, progress.current_season, progress.current_episode)

        assert progress.show_name == show.name
        assert progress.show_poster_path == show.poster_path
        assert progress.show_status == show.status_value
        assert progress.show_genres == show.genres
        assert progress.show_languages == show.languages
        assert progress.next_season == 3
        assert progress.next_episode == 2
        assert progress.next_air_date == "2019-10-05"
        assert progress.last_aired_season == show.last_aired_episode[0]
        assert progress.last_aired_episode == show.last_aired_episode[1]

        stop_if_finished.assert_called_once_with()

        save_progress.assert_called_once_with(progress)

    @pytest.mark.asyncio
    async def test_save_progress(self, mocker, command):
        progress = mocker.MagicMock(spec=Progress)
        await command._save_progress(progress)
        progress.save.assert_called_once_with()

    @pytest.mark.asyncio
    async def test_get_show(self, mocker, command):
        show_id = 123
        fetch = mocker.patch(f"{self.mock_path}.Command._fetch", return_value={"id": show_id})

        show = await command._get_show(show_id)

        assert show.id == show_id
        fetch.assert_awaited_once_with(f"{settings.TMDB_API_URL}/tv/{show_id}")

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

        get_air_date = mocker.patch(
            f"{self.mock_path}.Command._get_air_date", return_value=expected[2]
        )

        assert await command._get_next(show, 2, 3) == expected

        show.get_next_episode.assert_called_once_with(2, 3)

        if all(returned):
            get_air_date.assert_awaited_once_with(1, expected[0], expected[1])
        else:
            get_air_date.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "data,air_date",
        [({"air_date": "2019-10-05"}, "2019-10-05"), ({"air_date": ""}, None), ({}, None)],
    )
    async def test_get_air_date(self, mocker, command, data, air_date):
        fetch = mocker.patch(f"{self.mock_path}.Command._fetch", return_value=data)
        assert await command._get_air_date(1, 2, 3) == air_date
        fetch.assert_awaited_once_with(f"{settings.TMDB_API_URL}/tv/1/season/2/episode/3")

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", [200, 204, 400, 401, 404, 500, 503])
    async def test_fetch(self, mocker, command, status_code):
        data = {"foo": 123}

        response = mocker.MagicMock()
        response.status_code = status_code
        response.json.return_value = data

        client = AsyncMock(httpx.AsyncClient)
        client.get.return_value = response

        async_client = mocker.patch(f"{self.mock_path}.httpx.AsyncClient")
        async_client.return_value.__aenter__.return_value = client

        url = "/foo/bar"

        assert await command._fetch(url) == data

        client.get.assert_awaited_once_with(url, params={"api_key": settings.TMDB_API_KEY})

        if status_code == 404:
            response.raise_for_status.assert_not_called()
        else:
            response.raise_for_status.assert_called_once_with()

        response.json.assert_called_once_with()
