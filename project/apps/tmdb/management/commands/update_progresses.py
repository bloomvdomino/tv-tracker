import asyncio
from time import sleep

import httpx
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.management.base import BaseCommand

from project.apps.tmdb.models import Progress
from project.apps.tmdb.utils import Show


class Command(BaseCommand):
    @async_to_sync
    async def handle(self, *args, **options):
        n = 15
        progresses = Progress.objects.all()
        progress_chunks = [progresses[i : i + n] for i in range(0, progresses.count(), n)]

        for i, progresses in enumerate(progress_chunks):
            await asyncio.gather(*[self._update_progress(progress) for progress in progresses])

            if i < len(progress_chunks) - 1:
                sleep(11)

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
        progress.save()

    async def _get_show(self, show_id):
        url = f"{settings.TMDB_API_URL}tv/{show_id}"
        response = await self._fetch(url)
        if response.status_code == 404:
            return None
        return Show(response.json())

    async def _get_next(self, show, current_season, current_episode):
        next_season, next_episode = show.get_next_episode(current_season, current_episode)
        if not (next_season and next_episode):
            return None, None, None

        next_air_date = await self._get_air_date(show.id, next_season, next_episode)
        return next_season, next_episode, next_air_date

    async def _get_air_date(self, show_id, season, episode):
        url = f"{settings.TMDB_API_URL}tv/{show_id}/season/{season}/episode/{episode}"
        response = await self._fetch(url)

        # air_date from response data can be empty string, we want to return
        # None in this case.
        return response.json().get("air_date") or None

    async def _fetch(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"api_key": settings.TMDB_API_KEY})

        # We don't want to raise error on 404 response because:
        # 1) TMDB database can change, so the show ID saved in our database may
        #    no longer exist.
        # 2) Progresses with status not watched always have the first episode as
        #    the next episode in our database, but may not exist in the TMDB
        #    database.
        if response.status_code != 404:
            response.raise_for_status()

        return response
