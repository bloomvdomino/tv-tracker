import asyncio

import aiohttp
import requests
from asgiref.sync import async_to_sync
from django.conf import settings
from django.urls import reverse


def format_episode_label(season, episode):
    return 'S{}E{}'.format('0{}'.format(season)[-2:], '0{}'.format(episode)[-2:])


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


def add_detail_urls(shows):
    for show in shows:
        detail_url = reverse('tmdb:v2_show', kwargs={'id': show['id']})
        show.update(detail_url=detail_url)
    return shows


def mark_saved_shows(shows, user):
    from .models import Progress  # imported here to avoid circular dependency

    if user.is_authenticated:
        show_ids = [show['id'] for show in shows]
        saved_show_ids = Progress.objects.filter(
            user=user,
            show_id__in=show_ids,
        ).values_list('show_id', flat=True)
        for show in shows:
            show.update(saved=show['id'] in saved_show_ids)
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
    shows = fetch('tv/popular', params={'page': page})['results']
    return add_detail_urls(shows)


def search_show(name):
    """
    Search for TV shows by name.

    https://developers.themoviedb.org/3/search/search-tv-shows
    """
    shows = fetch('search/tv', params={'query': name})['results']
    return add_detail_urls(shows)


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
