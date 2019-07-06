import asyncio

import aiohttp
import requests
from asgiref.sync import async_to_sync
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property


class _Show:
    def __init__(self, data, user=None):
        self._data = data
        self._set_progress_related(user)

    @property
    def id(self):
        return self._data["id"]

    @property
    def name(self):
        return self._data["original_name"]

    @property
    def poster_path(self):
        return self._data["poster_path"]

    @property
    def vote_average(self):
        return self._data["vote_average"]

    @property
    def genres(self):
        return self._data["genres"]

    @property
    def languages(self):
        return self._data["languages"]

    @property
    def overview(self):
        return self._data["overview"]

    @property
    def status_display(self):
        return self._data["status"]

    @cached_property
    def status_value(self):
        from .models import Progress  # imported here to avoid circular dependency

        value_display_map = dict(Progress.SHOW_STATUS_CHOICES)
        display_value_map = {display: value for value, display in value_display_map.items()}
        return display_value_map[self.status_display]

    @cached_property
    def aired_episodes(self):
        aired_episodes = []
        for season, season_data in enumerate(self._seasons, 1):
            for episode in range(1, season_data["episode_count"] + 1):
                if not self._episode_aired(season, episode):
                    break
                aired_episodes.append((season, episode))
        return aired_episodes

    def _episode_aired(self, season, episode):
        last_aired_season, last_aired_episode = self.last_aired_episode
        if not (last_aired_season and last_aired_episode):
            return False
        return not (
            season > last_aired_season
            or (season == last_aired_season and episode > last_aired_episode)
        )

    @cached_property
    def last_aired_episode(self):
        last_aired = self._data["last_episode_to_air"]
        if not last_aired:
            return None, None
        return last_aired["season_number"], last_aired["episode_number"]

    def get_next_episode(self, season, episode):
        if not (season and episode):
            return 1, 1
        if episode < self._seasons[season - 1]["episode_count"]:
            # Not the last episode in the season.
            return season, episode + 1
        if season < len(self._seasons):
            # Not the last seasons.
            return season + 1, 1
        return None, None

    @cached_property
    def _seasons(self):
        """
        Return only non-special and non-empty seasons of the show.

        TMDb API may return some especial seasons as the first element in the
        list. And the last season may be empty.
        """
        seasons = self._data["seasons"]
        if seasons[0]["season_number"] == 0:
            del seasons[0]
        if not seasons[-1]:
            del seasons[-1]
        return seasons

    def _set_progress_related(self, user):
        self.saved = False
        if user and user.is_authenticated:
            self.saved = user.progress_set.filter(show_id=self.id).exists()
        action = "update" if self.saved else "create"
        self.edit_url = reverse("tmdb:progress_{}".format(action), kwargs={"show_id": self.id})


def format_episode_label(season, episode):
    season = "0{}".format(season)[-2:] if season < 100 else season
    episode = "0{}".format(episode)[-2:] if episode < 100 else episode
    return "S{}E{}".format(season, episode)


def fetch(endpoint, params=None):
    if not settings.TMDB_API_KEY:
        raise Exception("TMDB_API_KEY not provided.")

    url = "https://api.themoviedb.org/3/{}".format(endpoint)
    params = params or {}
    params.update(api_key=settings.TMDB_API_KEY)
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return res.json()


def get_show(id, user=None):
    """
    Get a TV show detail by ID.

    https://developers.themoviedb.org/3/tv/get-tv-details
    """
    data = fetch("tv/{}".format(id))
    return _Show(data, user=user)


def get_air_date(show_id, season, episode):
    endpoint = "tv/{}/season/{}/episode/{}".format(show_id, season, episode)
    return fetch(endpoint).get("air_date")


def get_popular_shows(page, user=None):
    """
    Get popular TV shows by page.

    https://developers.themoviedb.org/3/tv/get-popular-tv-shows
    """
    results = fetch("tv/popular", params={"page": page})["results"]
    return [_Show(data, user=user) for data in results]


def search_show(name, user=None):
    """
    Search for TV shows by name.

    https://developers.themoviedb.org/3/search/search-tv-shows
    """
    results = fetch("search/tv", params={"query": name})["results"]
    return [_Show(data, user=user) for data in results]


async def async_fetch(session, endpoint, params=None, **extras):
    url = "https://api.themoviedb.org/3/{}".format(endpoint)
    params = params or {}
    params.update(api_key=settings.TMDB_API_KEY)
    async with session.get(url, params=params) as resp:
        data = await resp.json()
    for key, value in extras.items():
        data[key] = value
    return data


@async_to_sync
async def get_shows(ids, user=None):
    async with aiohttp.ClientSession() as session:
        coros = [async_fetch(session, "tv/{}".format(id)) for id in ids]
        results = await asyncio.gather(*coros)
        return [_Show(data, user=user) for data in results]


@async_to_sync
async def get_air_dates(params_list):
    async with aiohttp.ClientSession() as session:
        coros = []
        for params in params_list:
            endpoint = "tv/{show_id}/season/{season}/episode/{episode}".format(**params)
            coros.append(async_fetch(session, endpoint, show_id=params["show_id"]))
        results = await asyncio.gather(*coros)
        return [result for result in results if result.get("air_date")]
