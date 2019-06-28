import pytest

from ..forms import ProgressForm
from ..utils import _Show
from .factories import ProgressFactory


class TestProgressForm:
    @pytest.fixture
    def instance(self):
        return ProgressFactory.build(next_air_date=None)

    @pytest.fixture
    def show(self, mocker):
        return mocker.MagicMock(spec=_Show)

    @pytest.fixture
    def update_next_air_date(self, mocker):
        return mocker.patch("project.apps.tmdb.models.Progress.update_next_air_date")

    def test_init(self, show, mocker):
        make_episode_choices = mocker.patch(
            "project.apps.tmdb.forms.ProgressForm._make_episode_choices", return_value=[1, 2]
        )
        form = ProgressForm(user=None, show=show)

        assert form.user is None
        assert form.show == show
        assert form.fields["last_watched"].choices == [1, 2]
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
        ],
    )
    def test_update_episodes(
        self, instance, show, update_next_air_date, current_episode, next_episode
    ):
        show.get_next_episode.return_value = next_episode
        cleaned_data = {
            "current_season": current_episode[0],
            "current_episode": current_episode[1],
        }
        form = ProgressForm(instance=instance, user=None, show=show)
        form.cleaned_data = cleaned_data

        form._update_episodes()

        assert form.instance.current_season == current_episode[0]
        assert form.instance.current_episode == current_episode[1]
        assert form.instance.next_season == next_episode[0]
        assert form.instance.next_episode == next_episode[1]

        update_next_air_date.assert_called_once_with()
