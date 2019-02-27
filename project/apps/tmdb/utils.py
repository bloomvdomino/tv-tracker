import requests
from django.conf import settings
from django.urls import reverse


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


def get_show(id):
    """
    Get a TV show detail by ID.
    https://developers.themoviedb.org/3/tv/get-tv-details
    """
    url = 'https://api.themoviedb.org/3/tv/{}'.format(id)
    params = {'api_key': settings.TMDB_API_KEY}
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return res.json()


def get_popular_shows(page):
    """
    Get popular TV shows by page.
    https://developers.themoviedb.org/3/tv/get-popular-tv-shows
    """
    url = 'https://api.themoviedb.org/3/tv/popular'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'page': page,
    }
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return add_detail_links(res.json()['results'])


def search_show(name):
    """
    Search for TV shows by name.
    https://developers.themoviedb.org/3/search/search-tv-shows
    """
    url = 'https://api.themoviedb.org/3/search/tv'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'query': name,
    }
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return add_detail_links(res.json()['results'])
