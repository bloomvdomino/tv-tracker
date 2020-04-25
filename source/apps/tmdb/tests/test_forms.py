import pytest

from source.apps.accounts.tests.factories import UserFactory
from source.apps.tmdb.forms import FilterForm, ProgressForm
from source.apps.tmdb.tests.factories import ProgressFactory
from source.apps.tmdb.utils import Show


class TestFilterForm:
    @pytest.mark.django_db
    def test(self):
        user = UserFactory()
        ProgressFactory(
            user=user, show_id=1, show_genres=["Action", "Drama"], show_languages=["en"]
        )
        ProgressFactory(user=user, show_id=2, show_genres=["Drama"], show_languages=["ko", "en"])
        ProgressFactory(user=user, show_id=3, show_genres=["Comedy"], show_languages=["zh"])

        ProgressFactory(user=UserFactory(email="u2@tt.com"), show_id=4, show_languages=["pt"])

        form = FilterForm(user=user)

        assert form.user == user
        assert form.fields["genre"].choices == [
            ("", "-"),
            ("Action", "Action"),
            ("Comedy", "Comedy"),
            ("Drama", "Drama"),
        ]
        assert form.fields["language"].choices == [
            ("", "-"),
            ("en", "EN"),
            ("ko", "KO"),
            ("zh", "ZH"),
        ]


class TestProgressForm:
    @pytest.fixture
    def show(self, mocker):
        return mocker.MagicMock(spec=Show)

    @pytest.fixture
    def episode_choices(self):
        return [("0-0", "Not started."), ("1-1", "S01E01"), ("1-2", "S01E02")]

    @pytest.fixture
    def make_episode_choices(self, mocker, episode_choices):
        return mocker.patch(
            "source.apps.tmdb.forms.ProgressForm._make_episode_choices",
            return_value=episode_choices,
        )

    def test_init(self, show, make_episode_choices, episode_choices):
        form = ProgressForm(show=show)

        assert form.show == show
        assert form.fields["last_watched"].choices == episode_choices
        make_episode_choices.assert_called_once_with()

    @pytest.mark.parametrize(
        "current_episode,next_episode",
        [
            ((0, 0), (None, None)),
            ((0, 0), (1, None)),
            ((0, 0), (None, 1)),
            ((0, 0), (1, 1)),
            ((1, 1), (None, None)),
            ((1, 1), (1, None)),
            ((1, 1), (None, 1)),
            ((1, 1), (1, 2)),
            ((5, 10), (6, 1)),
        ],
    )
    def test_clean_last_watched(
        self, mocker, current_episode, next_episode, show, make_episode_choices
    ):
        show.get_next_episode.return_value = next_episode
        last_watched = f"{current_episode[0]}-{current_episode[1]}"
        form = ProgressForm(show=show)
        form.cleaned_data = {"last_watched": last_watched}

        assert form.clean_last_watched() == last_watched

        assert form.instance.current_season == current_episode[0]
        assert form.instance.current_episode == current_episode[1]
        assert form.instance.next_season == next_episode[0]
        assert form.instance.next_episode == next_episode[1]
