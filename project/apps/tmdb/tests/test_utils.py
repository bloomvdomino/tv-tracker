import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import resolve

from project.apps.accounts.tests.factories import UserFactory

from ..models import Progress
from ..utils import _Show, format_episode_label, get_air_date
from .factories import ProgressFactory


class TestShow:
    @pytest.fixture
    def mock_set_progress_related(self, mocker):
        return mocker.patch("project.apps.tmdb.utils._Show._set_progress_related")

    @pytest.mark.parametrize("user", [None, UserFactory.build()])
    def test__init__(self, mock_set_progress_related, user):
        data = {"id": 123}
        show = _Show(data, user=user) if user else _Show(data)

        assert show._data == data
        show._set_progress_related.assert_called_once_with(user)

    def test_id(self, mock_set_progress_related):
        show = _Show({"id": 123})
        assert show.id == 123

    def test_name(self, mock_set_progress_related):
        show = _Show({"original_name": "Impastor"})
        assert show.name == "Impastor"

    def test_poster_path(self, mock_set_progress_related):
        show = _Show({"poster_path": "/foo/bar.jpg"})
        assert show.poster_path == "/foo/bar.jpg"

    def test_vote_average(self, mock_set_progress_related):
        show = _Show({"vote_average": 8.3})
        assert show.vote_average == 8.3

    def test_genres(self, mock_set_progress_related):
        show = _Show({"genres": ["foo", "bar"]})
        assert show.genres == ["foo", "bar"]

    def test_languages(self, mock_set_progress_related):
        show = _Show({"languages": ["foo"]})
        assert show.languages == ["foo"]

    def test_overview(self, mock_set_progress_related):
        show = _Show({"overview": "Foo bar."})
        assert show.overview == "Foo bar."

    @pytest.mark.parametrize("display", [display for _, display in Progress.SHOW_STATUS_CHOICES])
    def test_status_display(self, mock_set_progress_related, display):
        data = {"status": display}
        show = _Show(data)
        assert show.status_display == display

    @pytest.mark.parametrize("value,display", Progress.SHOW_STATUS_CHOICES)
    def test_status_value(self, mock_set_progress_related, value, display):
        data = {"status": display}
        show = _Show(data)
        assert show.status_value == value

    def test_aired_episodes(self, mocker, mock_set_progress_related):
        mocker.patch(
            "project.apps.tmdb.utils._Show._seasons",
            new=mocker.PropertyMock(return_value=[{"episode_count": 3}, {"episode_count": 3}]),
        )
        mocker.patch(
            "project.apps.tmdb.utils._Show.last_aired_episode",
            new=mocker.PropertyMock(return_value=(2, 1)),
        )

        show = _Show({})
        assert show.aired_episodes == [(1, 1), (1, 2), (1, 3), (2, 1)]

    @pytest.mark.parametrize(
        "last_aired,season,episode,aired",
        [
            ((None, None), 1, 1, False),
            ((2, None), 1, 1, False),
            ((None, 2), 1, 1, False),
            ((2, 3), 1, 2, True),
            ((2, 3), 1, 3, True),
            ((2, 3), 1, 4, True),
            ((2, 3), 2, 2, True),
            ((2, 3), 2, 3, True),
            ((2, 3), 2, 4, False),
            ((2, 3), 3, 2, False),
            ((2, 3), 3, 3, False),
            ((2, 3), 3, 4, False),
        ],
    )
    def test_episode_aired(
        self, mocker, mock_set_progress_related, last_aired, season, episode, aired
    ):
        mocker.patch(
            "project.apps.tmdb.utils._Show.last_aired_episode",
            new=mocker.PropertyMock(return_value=last_aired),
        )
        show = _Show({})
        assert show._episode_aired(season, episode) is aired

    @pytest.mark.parametrize(
        "last_episode_to_air,expected",
        [(None, (None, None)), ({"season_number": 1, "episode_number": 2}, (1, 2))],
    )
    def test_last_aired_episode(self, mock_set_progress_related, last_episode_to_air, expected):
        data = {"last_episode_to_air": last_episode_to_air}
        show = _Show(data)
        assert show.last_aired_episode == expected

    @pytest.mark.parametrize(
        "episode,expected",
        [
            ((None, None), (1, 1)),
            ((0, 0), (1, 1)),
            ((1, 1), (1, 2)),
            ((1, 2), (1, 3)),
            ((1, 3), (2, 1)),
            ((2, 1), (2, 2)),
            ((2, 2), (2, 3)),
            ((2, 3), (None, None)),
        ],
    )
    def test_get_next_episode(self, mocker, mock_set_progress_related, episode, expected):
        mocker.patch(
            "project.apps.tmdb.utils._Show._seasons",
            new=mocker.PropertyMock(return_value=[{"episode_count": 3}, {"episode_count": 3}]),
        )
        show = _Show({})
        assert show.get_next_episode(*episode) == expected

    @pytest.mark.parametrize(
        "seasons,expected",
        [
            (
                [{"season_number": 0}, {"season_number": 1}, {"season_number": 2}],
                [{"season_number": 1}, {"season_number": 2}],
            ),
            (
                [{"season_number": 1}, {"season_number": 2}, {}],
                [{"season_number": 1}, {"season_number": 2}],
            ),
            (
                [{"season_number": 0}, {"season_number": 1}, {"season_number": 2}, {}],
                [{"season_number": 1}, {"season_number": 2}],
            ),
            (
                [{"season_number": 1}, {"season_number": 2}],
                [{"season_number": 1}, {"season_number": 2}],
            ),
        ],
    )
    def test_seasons(self, mock_set_progress_related, seasons, expected):
        data = {"seasons": seasons}
        show = _Show(data)
        assert show._seasons == expected

    @pytest.mark.parametrize("user", [None, AnonymousUser()])
    def test_set_progress_related_none_or_anonymous_user(self, user):
        show = _Show({"id": 123}, user=user)

        assert not show.saved

        resolved = resolve(show.edit_url)
        assert resolved.namespace == "tmdb"
        assert resolved.url_name == "progress_create"
        assert resolved.kwargs == {"show_id": 123}

    @pytest.mark.django_db
    @pytest.mark.parametrize("saved,action", [(True, "update"), (False, "create")])
    def test_set_progress_related_authenticated_user(self, saved, action):
        show_id = 123
        user = UserFactory()
        ProgressFactory(user=user, show_id=show_id if saved else 321)
        show = _Show({"id": show_id}, user=user)

        assert show.saved is saved

        resolved = resolve(show.edit_url)
        assert resolved.namespace == "tmdb"
        assert resolved.url_name == "progress_{}".format(action)
        assert resolved.kwargs == {"show_id": show_id}


class TestFormatEpisodeLabel:
    @pytest.mark.parametrize(
        "season,episode,label",
        [
            (1, 1, "S01E01"),
            (1, 10, "S01E10"),
            (10, 1, "S10E01"),
            (10, 10, "S10E10"),
            (1, 101, "S01E101"),
            (100, 1, "S100E01"),
            (100, 101, "S100E101"),
        ],
    )
    def test(self, season, episode, label):
        assert format_episode_label(season, episode) == label


class TestGetAirDate:
    def test_with_air_date(self, mocker):
        fetch = mocker.patch(
            "project.apps.tmdb.utils.fetch", return_value={"air_date": "2019-6-30"}
        )

        air_date = get_air_date("123", 1, 2)

        assert air_date == "2019-6-30"
        fetch.assert_called_once_with("tv/123/season/1/episode/2")

    def test_without_air_date(self, mocker):
        fetch = mocker.patch("project.apps.tmdb.utils.fetch", return_value={})

        air_date = get_air_date("123", 1, 2)

        assert air_date is None
        fetch.assert_called_once_with("tv/123/season/1/episode/2")
