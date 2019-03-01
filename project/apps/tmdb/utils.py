import requests
from django.conf import settings
from django.urls import reverse

from .models import Progress


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


def add_detail_links(shows):
    for show in shows:
        detail_link = reverse('tmdb:v2_show', kwargs={'id': show['id']})
        show.update(detail_link=detail_link)
    return shows


def mark_saved_shows(shows, user):
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


def get_popular_shows(page):
    """
    Get popular TV shows by page.

    https://developers.themoviedb.org/3/tv/get-popular-tv-shows
    """
    shows = fetch('tv/popular', params={'page': page})['results']
    return add_detail_links(shows)


def search_show(name):
    """
    Search for TV shows by name.

    https://developers.themoviedb.org/3/search/search-tv-shows
    """
    shows = fetch('search/tv', params={'query': name})['results']
    return add_detail_links(shows)
