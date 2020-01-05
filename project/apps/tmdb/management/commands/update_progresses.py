import asyncio
from time import sleep

import httpx
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from sentry_sdk import capture_exception

from project.apps.tmdb.models import Progress
from project.apps.tmdb.utils import Show


class Command(BaseCommand):
    @async_to_sync
    async def handle(self, *args, **options):
        progress_chunks = await self._get_progress_chunks(15)

        for i, progresses in enumerate(progress_chunks):
            results = await asyncio.gather(
                *[self._update_progress(progress) for progress in progresses],
                return_exceptions=True,
            )
            self._capture_exceptions(results)

            if i < len(progress_chunks) - 1:
                sleep(11)

    @sync_to_async
    def _get_progress_chunks(self, size):
        """
        Avoid the SynchronousOnlyOperation error.
        https://docs.djangoproject.com/en/3.0/topics/async/
        """
        # Converting to list so it executes the query now.
        progresses = list(Progress.objects.all())
        return [progresses[i : i + size] for i in range(0, len(progresses), size)]

    def _capture_exceptions(self, results):
        for result in results:
            if isinstance(result, Exception):
                capture_exception(result)

    async def _update_progress(self, progress):
        show = await self._get_show(progress.show_id)
        if not show:
            return

        next_season, next_episode, next_air_date = await self._get_next(
            show, progress.current_season, progress.current_episode
        )

        last_aired_season, last_aired_episode = show.last_aired_episode

        progress.show_name = show.name
        progress.show_poster_path = show.poster_path
        progress.show_status = show.status_value
        progress.next_season = next_season
        progress.next_episode = next_episode
        progress.next_air_date = next_air_date
        progress.last_aired_season = last_aired_season
        progress.last_aired_episode = last_aired_episode
        progress.stop_if_finished()
        await self._save_progress(progress)

    @sync_to_async
    def _save_progress(self, progress):
        """
        Avoid the SynchronousOnlyOperation error.
        https://docs.djangoproject.com/en/3.0/topics/async/
        """
        progress.save()

    async def _get_show(self, show_id):
        url = f"{settings.TMDB_API_URL}tv/{show_id}"
        data = await self._fetch(url)
        return Show(data)

    async def _get_next(self, show, current_season, current_episode):
        next_season, next_episode = show.get_next_episode(current_season, current_episode)
        if not (next_season and next_episode):
            return None, None, None

        next_air_date = await self._get_air_date(show.id, next_season, next_episode)
        return next_season, next_episode, next_air_date

    async def _get_air_date(self, show_id, season, episode):
        url = f"{settings.TMDB_API_URL}tv/{show_id}/season/{season}/episode/{episode}"
        data = await self._fetch(url)

        # air_date from response data can be empty string, we want to return
        # None in this case.
        return data.get("air_date") or None

    async def _fetch(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"api_key": settings.TMDB_API_KEY})

        # Fetching next episode may return 404, but we shouldn't treat it as an
        # error.
        if response.status_code != 404:
            response.raise_for_status()

        return response.json()
