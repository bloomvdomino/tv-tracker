import pytest

from source.apps.tmdb.templatetags.tmdb import poster_url


class TestPosterUrl:
    @pytest.mark.parametrize(
        "i,width",
        [
            (0, "original"),
            (1, "w92"),
            (2, "w154"),
            (3, "w185"),
            (4, "w342"),
            (5, "w500"),
            (6, "w780"),
        ],
    )
    def test(self, i, width):
        path = "/foo.jpg"
        url = poster_url(path, i)
        assert url == f"https://image.tmdb.org/t/p/{width}{path}"
