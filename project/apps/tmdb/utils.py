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


def search_by_name(name):
    url = 'https://api.themoviedb.org/3/search/tv'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'query': name,
        'language': 'en-US',
    }
    res = requests.get(url, params=params)
    # TODO: handle status code other than 200.
    return res.json()['results']
