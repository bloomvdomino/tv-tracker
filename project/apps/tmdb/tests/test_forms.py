import pytest

from project.apps.accounts.tests.factories import UserFactory

from ..forms import ProgressForm
from ..models import Progress
from ..utils import _Show
from .factories import ProgressFactory


class TestProgressForm:
    @pytest.fixture
    def show(self, mocker):
        return mocker.MagicMock(spec=_Show)

    @pytest.fixture
    def update_show_data(self, mocker):
        return mocker.patch("project.apps.tmdb.models.Progress.update_show_data")

    @pytest.fixture
    def make_episode_choices(self, mocker):
        return mocker.patch(
            "project.apps.tmdb.forms.ProgressForm._make_episode_choices", return_value=[1, 2]
        )

    def test_init_when_not_updating(self, show, update_show_data, make_episode_choices):
        form = ProgressForm(user=None, show=show)

        assert form.user is None
        assert form.show == show
        assert form.fields["last_watched"].choices == [1, 2]
        make_episode_choices.assert_called_once_with()
        update_show_data.assert_not_called()

    def test_init_when_updating(self, show, update_show_data, make_episode_choices):
        instance = ProgressFactory.build()
        form = ProgressForm(instance=instance, user=None, show=show)

        assert form.user is None
        assert form.show == show
        assert form.fields["last_watched"].choices == [1, 2]
        make_episode_choices.assert_called_once_with()
        update_show_data.assert_called_once_with()

    @pytest.mark.django_db
    def test_save_when_not_updating(self, mocker, update_show_data):
        update_episodes = mocker.patch("project.apps.tmdb.forms.ProgressForm._update_episodes")
        user = UserFactory()
        show = mocker.MagicMock()
        type(show).id = mocker.PropertyMock(return_value=123)
        data = {"status": Progress.PAUSED, "last_watched": "0-0"}
        form = ProgressForm(data=data, user=user, show=show)

        assert form.is_valid()
        progress = form.save()

        update_episodes.assert_called_once_with()
        update_show_data.assert_called_once_with()

        assert progress.user == user
        assert progress.status == data["status"]
        assert progress.show_id == show.id
        assert progress.current_season == 0
        assert progress.current_episode == 0

    @pytest.mark.django_db
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
        self,
        mocker,
        show,
        update_show_data,
        make_episode_choices,
        current_episode,
        next_episode,
        settings,
    ):
        update_next_air_date = mocker.patch(
            "project.apps.tmdb.models.Progress.update_next_air_date"
        )
        show.get_next_episode.return_value = next_episode
        cleaned_data = {
            "current_season": current_episode[0],
            "current_episode": current_episode[1],
        }
        instance = ProgressFactory(next_air_date=None)
        form = ProgressForm(instance=instance, user=None, show=show)
        form.cleaned_data = cleaned_data

        form._update_episodes()

        assert form.instance.current_season == current_episode[0]
        assert form.instance.current_episode == current_episode[1]
        assert form.instance.next_season == next_episode[0]
        assert form.instance.next_episode == next_episode[1]

        update_next_air_date.assert_called_once_with()
