import requests
from django.conf import settings


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


def get_popular_shows(page):
    """
    Get popular TV shows.
    https://developers.themoviedb.org/3/tv/get-popular-tv-shows
    """
    url = 'https://api.themoviedb.org/3/tv/popular'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'page': page,
    }
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return res.json()['results']


def search_by_name(name):
    """
    Search for a TV show by name.
    https://developers.themoviedb.org/3/search/search-tv-shows
    """
    url = 'https://api.themoviedb.org/3/search/tv'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'query': name,
    }
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return res.json()['results']
