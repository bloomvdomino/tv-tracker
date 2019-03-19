import asyncio

import aiohttp
import requests
from asgiref.sync import async_to_sync
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property


class Show:
    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return self._data['id']

    @cached_property
    def status_value(self):
        from .models import Progress  # imported here to avoid circular dependency

        for value, display in Progress.SHOW_STATUS_CHOICES:
            if display == self.status_display:
                return value

    @cached_property
    def status_display(self):
        return self._data['status']

    @cached_property
    def aired_episodes(self):
        aired_episodes = []
        for season, season_data in enumerate(self._seasons, 1):
            for episode in range(1, season_data['episode_count'] + 1):
                if not self._episode_aired(season, episode):
                    break
                aired_episodes.append((season, episode))
        return aired_episodes

    def _episode_aired(self, season, episode):
        if not self._last_aired_episode:
            return False

        last_aired_season, last_aired_episode = self._last_aired_episode
        return not (
            season > last_aired_season or
            (season == last_aired_season and episode > last_aired_episode)
        )

    @cached_property
    def _last_aired_episode(self):
        last_aired = self._data['last_episode_to_air']
        if not last_aired:
            return None
        return last_aired['season_number'], last_aired['episode_number']

    def get_next_episode(self, season, episode):
        if not (season and episode):
            return 1, 1
        if episode < self._seasons[season - 1]['episode_count']:
            # Not the last episode in the season.
            return season, episode + 1
        if season < len(self._seasons):
            # Not the last seasons.
            return season + 1, 1
        return None

    @cached_property
    def _seasons(self):
        """
        Return only non-special and non-empty seasons of the show.

        TMDb API may return some especial seasons as the first element in the
        list. And the last season may be empty.
        """
        seasons = self._data['seasons']
        if seasons[0]['season_number'] == 0:
            del seasons[0]
        if not seasons[-1]:
            del seasons[-1]
        return seasons

    def set_user_related(self, user):
        self.saved = False
        if user.is_authenticated:
            self.saved = user.progress_set.filter(show_id=self.id).exists()
        action = 'update' if self.saved else 'create'
        self.edit_url = reverse('tmdb:progress_{}'.format(action), kwargs={'show_id': self.id})


def format_episode_label(season, episode):
    season = '0{}'.format(season)[-2:] if season < 100 else season
    episode = '0{}'.format(episode)[-2:] if episode < 100 else episode
    return 'S{}E{}'.format(season, episode)


def get_status_value(text):
    from .models import Progress  # imported here to avoid circular dependency

    for value, display in Progress.SHOW_STATUS_CHOICES:
        if display == text:
            return value


def make_poster_url(path, width):
    widths = [
        'original',
        'w92',
        'w154',
        'w185',
        'w342',
        'w500',
        'w780',
    ]
    return 'https://image.tmdb.org/t/p/{}{}'.format(widths[width], path)


def add_progress_info(shows, user):
    if not user.is_authenticated:
        for show in shows:
            show.update(edit_url=reverse('tmdb:progress_create', kwargs={'show_id': show['id']}))
    else:
        show_ids = [show['id'] for show in shows]
        saved_show_ids = user.progress_set.filter(show_id__in=show_ids).values_list('show_id', flat=True)
        for show in shows:
            saved = show['id'] in saved_show_ids
            action = 'update' if saved else 'create'
            edit_url = reverse('tmdb:progress_{}'.format(action), kwargs={'show_id': show['id']})
            show.update(saved=saved, edit_url=edit_url)
    return shows


def filter_seasons(show):
    """
    Return only non-special and non-empty seasons of the show.

    TMDB API may also return some especial seasons as the first element in the
    list. And the last season may be empty.
    """
    n = len(show['seasons']) - show['number_of_seasons']
    seasons = show['seasons'][n:]
    if not seasons[-1]:
        del seasons[-1]
    show.update(seasons=seasons)
    return show


def episode_aired(season, episode, last_aired_season, last_aired_episode):
    return not (
        season > last_aired_season or
        (season == last_aired_season and episode > last_aired_episode)
    )


def get_aired_episodes(show):
    last_aired = show.get('last_episode_to_air', {})
    last_aired_season = last_aired.get('season_number', 0)
    last_aired_episode = last_aired.get('episode_number', 0)

    aired_episodes = []
    for season, info in enumerate(show['seasons'], 1):
        for episode in range(1, info['episode_count'] + 1):
            if not episode_aired(season, episode, last_aired_season, last_aired_episode):
                break
            aired_episodes.append((season, episode))
    return aired_episodes


def get_next_episode(show, season, episode):
    if season == 0 or episode == 0:
        return 1, 1

    seasons = filter_seasons(show)['seasons']
    if episode < seasons[season - 1]['episode_count']:
        # Not the last episode in the season.
        return season, episode + 1
    if season < len(seasons):
        # Not the last seasons.
        return season + 1, 1
    return None, None


def fetch(endpoint, params=None):
    url = 'https://api.themoviedb.org/3/{}'.format(endpoint)
    params = params or {}
    params.update(api_key=settings.TMDB_API_KEY)
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return res.json()


def get_show(id):
    """
    Get a TV show detail by ID.

    https://developers.themoviedb.org/3/tv/get-tv-details
    """
    return filter_seasons(fetch('tv/{}'.format(id)))


def get_air_date(show_id, season, episode):
    endpoint = 'tv/{}/season/{}/episode/{}'.format(show_id, season, episode)
    return fetch(endpoint)['air_date']


def get_popular_shows(page):
    """
    Get popular TV shows by page.

    https://developers.themoviedb.org/3/tv/get-popular-tv-shows
    """
    return fetch('tv/popular', params={'page': page})['results']


def search_show(name):
    """
    Search for TV shows by name.

    https://developers.themoviedb.org/3/search/search-tv-shows
    """
    return fetch('search/tv', params={'query': name})['results']


async def async_fetch(session, endpoint, params=None, **extras):
    url = 'https://api.themoviedb.org/3/{}'.format(endpoint)
    params = params or {}
    params.update(api_key=settings.TMDB_API_KEY)
    async with session.get(url, params=params) as resp:
        data = await resp.json()
    for key, value in extras.items():
        data[key] = value
    return data


@async_to_sync
async def get_shows(ids):
    async with aiohttp.ClientSession() as session:
        coros = [async_fetch(session, 'tv/{}'.format(id)) for id in ids]
        return await asyncio.gather(*coros)


@async_to_sync
async def get_air_dates(params_list):
    async with aiohttp.ClientSession() as session:
        coros = []
        for params in params_list:
            endpoint = 'tv/{show_id}/season/{season}/episode/{episode}'.format(**params)
            coros.append(async_fetch(session, endpoint, show_id=params['show_id']))
        return await asyncio.gather(*coros)
