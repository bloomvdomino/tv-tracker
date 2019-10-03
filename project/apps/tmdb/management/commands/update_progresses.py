import asyncio
from time import sleep

import httpx
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.management.base import BaseCommand

from project.apps.accounts.models import User
from project.apps.tmdb.models import Progress
from project.apps.tmdb.utils import Show


class Command(BaseCommand):
    def handle(self, *args, **options):
        show_ids = set(Progress.objects.values_list("show_id", flat=True))
        shows = self._fetch_shows(show_ids)

        updated_data = self._get_updated_progress_data(shows)
        updated_data = self._fetch_next_air_dates(updated_data)

        for progress_id, data in updated_data.items():
            Progress.objects.filter(id=progress_id).update(**data)
        for user in User.objects.all():
            user.stop_finished_shows()

    def _fetch_shows(self, show_ids):
        urls = [f"{settings.TMDB_API_URL}tv/{show_id}" for show_id in show_ids]
        responses = self._fetch_urls(urls)
        shows = [Show(response.json()) for response in responses]
        return {show.id: show for show in shows}

    def _get_updated_progress_data(self, shows):
        data = {}
        for progress in Progress.objects.all():
            show = shows[progress.show_id]
            next_season, next_episode = show.get_next_episode(
                progress.current_season, progress.current_episode
            )
            last_aired_season, last_aired_episode = show.last_aired_episode
            data[progress.id] = {
                "show_id": show.id,
                "show_name": show.name,
                "show_poster_path": show.poster_path,
                "show_status": show.status_value,
                "next_season": next_season,
                "next_episode": next_episode,
                "last_aired_season": last_aired_season,
                "last_aired_episode": last_aired_episode,
            }
        return data

    def _fetch_next_air_dates(self, progress_data):
        urls = []
        for data in progress_data.values():
            season = data["next_season"]
            episode = data["next_episode"]
            if not (season and episode):
                continue
            show_id = data["show_id"]
            urls.append(f"{settings.TMDB_API_URL}tv/{show_id}/season/{season}/episode/{episode}")

        responses = self._fetch_urls(urls)
        escaped = 0
        for i, data in enumerate(progress_data.values()):
            if not (data["next_season"] and data["next_episode"]):
                escaped += 1
                continue
            data["next_air_date"] = responses[i - escaped].json().get("air_date")
        return progress_data

    @async_to_sync
    async def _fetch_urls(self, urls):
        chunk_size = settings.TMDB_FETCH_CHUNK_SIZE
        url_chunks = [urls[i : i + chunk_size] for i in range(0, len(urls), chunk_size)]

        responses = []
        for i, url_chunk in enumerate(url_chunks):
            responses += await asyncio.gather(*[self._fetch_url(url) for url in url_chunk])
            if i < len(url_chunks) - 1:
                sleep(11)
        return responses

    async def _fetch_url(self, url):
        client = httpx.AsyncClient()
        response = await client.get(url, params={"api_key": settings.TMDB_API_KEY})
        response.raise_for_status()
        return response
