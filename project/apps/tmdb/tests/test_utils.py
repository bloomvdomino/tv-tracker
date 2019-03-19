import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import resolve

from project.apps.accounts.tests.factories import UserFactory

from ..models import Progress
from ..utils import Show, format_episode_label
from .factories import ProgressFactory


class TestShow:
    def test__init__(self):
        data = {'id': 123}
        show = Show(data)
        assert show._data == data

    def test_id(self):
        data = {'id': 123}
        show = Show(data)
        assert show.id == 123

    @pytest.mark.parametrize('value,display', Progress.SHOW_STATUS_CHOICES)
    def test_status_value(self, value, display):
        data = {'status': display}
        show = Show(data)
        assert show.status_value == value

    @pytest.mark.parametrize('display', [display for _, display in Progress.SHOW_STATUS_CHOICES])
    def test_status_display(self, display):
        data = {'status': display}
        show = Show(data)
        assert show.status_display == display

    def test_aired_episodes(self, mocker):
        mocker.patch(
            'project.apps.tmdb.utils.Show._seasons',
            new=mocker.PropertyMock(return_value=[
                {'episode_count': 3},
                {'episode_count': 3},
            ]),
        )
        mocker.patch(
            'project.apps.tmdb.utils.Show._last_aired_episode',
            new=mocker.PropertyMock(return_value=(2, 1)),
        )

        show = Show({})
        assert show.aired_episodes == [
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 1),
        ]

    @pytest.mark.parametrize('last_aired,season,episode,aired', [
        (None, 1, 1, False),
        ((2, 3), 1, 2, True),
        ((2, 3), 1, 3, True),
        ((2, 3), 1, 4, True),
        ((2, 3), 2, 2, True),
        ((2, 3), 2, 3, True),
        ((2, 3), 2, 4, False),
        ((2, 3), 3, 2, False),
        ((2, 3), 3, 3, False),
        ((2, 3), 3, 4, False),
    ])
    def test_episode_aired(self, mocker, last_aired, season, episode, aired):
        mocker.patch(
            'project.apps.tmdb.utils.Show._last_aired_episode',
            new=mocker.PropertyMock(return_value=last_aired),
        )
        show = Show({})
        assert show._episode_aired(season, episode) is aired

    @pytest.mark.parametrize('last_episode_to_air,expected', [
        (None, None),
        ({'season_number': 1, 'episode_number': 2}, (1, 2)),
    ])
    def test_last_aired_episode(self, last_episode_to_air, expected):
        data = {'last_episode_to_air': last_episode_to_air}
        show = Show(data)
        assert show._last_aired_episode == expected

    @pytest.mark.parametrize('episode,expected', [
        ((None, None), (1, 1)),
        ((0, 0), (1, 1)),
        ((1, 1), (1, 2)),
        ((1, 2), (1, 3)),
        ((1, 3), (2, 1)),
        ((2, 1), (2, 2)),
        ((2, 2), (2, 3)),
        ((2, 3), None),
    ])
    def test_get_next_episode(self, mocker, episode, expected):
        mocker.patch(
            'project.apps.tmdb.utils.Show._seasons',
            new=mocker.PropertyMock(return_value=[
                {'episode_count': 3},
                {'episode_count': 3},
            ]),
        )
        show = Show({})
        assert show.get_next_episode(*episode) == expected

    @pytest.mark.parametrize('seasons,expected', [
        (
            [
                {'season_number': 0},
                {'season_number': 1},
                {'season_number': 2},
            ],
            [
                {'season_number': 1},
                {'season_number': 2},
            ],
        ),
        (
            [
                {'season_number': 1},
                {'season_number': 2},
                {},
            ],
            [
                {'season_number': 1},
                {'season_number': 2},
            ],
        ),
        (
            [
                {'season_number': 0},
                {'season_number': 1},
                {'season_number': 2},
                {},
            ],
            [
                {'season_number': 1},
                {'season_number': 2},
            ],
        ),
        (
            [
                {'season_number': 1},
                {'season_number': 2},
            ],
            [
                {'season_number': 1},
                {'season_number': 2},
            ],
        ),
    ])
    def test_seasons(self, seasons, expected):
        data = {'seasons': seasons}
        show = Show(data)
        assert show._seasons == expected

    def test_set_user_related_anonymous_user(self):
        user = AnonymousUser()
        show = Show({'id': 123})
        show.set_user_related(user)

        assert not show.saved

        resolved = resolve(show.edit_url)
        assert resolved.namespace == 'tmdb'
        assert resolved.url_name == 'progress_create'
        assert resolved.kwargs == {'show_id': 123}

    @pytest.mark.django_db
    @pytest.mark.parametrize('saved,action', [
        (True, 'update'),
        (False, 'create'),
    ])
    def test_set_user_related_authenticated_user(self, saved, action):
        user = UserFactory()
        show_id = 123
        show = Show({'id': show_id})
        ProgressFactory(user=user, show_id=show_id if saved else 321)
        show.set_user_related(user)

        assert show.saved is saved

        resolved = resolve(show.edit_url)
        assert resolved.namespace == 'tmdb'
        assert resolved.url_name == 'progress_{}'.format(action)
        assert resolved.kwargs == {'show_id': show_id}


class TestFormatEpisodeLabel:
    @pytest.mark.parametrize('season,episode,label', [
        (1, 1, 'S01E01'),
        (1, 10, 'S01E10'),
        (10, 1, 'S10E01'),
        (10, 10, 'S10E10'),
        (1, 101, 'S01E101'),
        (100, 1, 'S100E01'),
        (100, 101, 'S100E101'),
    ])
    def test(self, season, episode, label):
        assert format_episode_label(season, episode) == label
