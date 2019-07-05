import pytest

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
        return mocker.patch("project.apps.tmdb.forms.ProgressForm._update_show_data")

    @pytest.fixture
    def make_episode_choices(self, mocker):
        return mocker.patch(
            "project.apps.tmdb.forms.ProgressForm._make_episode_choices", return_value=[1, 2]
        )

    def test_init(self, show, update_show_data, make_episode_choices):
        initial = {}
        instance = ProgressFactory.build()
        form = ProgressForm(initial=initial, instance=instance, user=None, show=show)

        assert form.user is None
        assert form.show == show
        assert form.fields["last_watched"].choices == [1, 2]
        update_show_data.assert_called_once_with(initial, instance)
        make_episode_choices.assert_called_once_with()

    @pytest.mark.django_db
    def test_update_show_data_called(self, show, make_episode_choices):
        initial = {
            "show_id": 1,
            "show_name": "Foo",
            "show_poster_path": "/foo.jpg",
            "show_status": Progress.ENDED,
            "last_watched": "1-2",
        }
        instance = ProgressFactory(next_air_date=None)

        ProgressForm(initial=initial, instance=instance, user=None, show=show)
        instance.refresh_from_db()

        assert instance.show_id == initial["show_id"]
        assert instance.show_name == initial["show_name"]
        assert instance.show_poster_path == initial["show_poster_path"]
        assert instance.show_status == initial["show_status"]

    def test_update_show_data_not_called(self, mocker, show, make_episode_choices):
        progress = mocker.MagicMock()
        progress.__bool__.return_value = False

        ProgressForm(initial={}, instance=progress, user=None, show=show)

        progress.save.assert_not_called()

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
        form = ProgressForm(initial={}, instance=instance, user=None, show=show)
        form.cleaned_data = cleaned_data

        form._update_episodes()

        assert form.instance.current_season == current_episode[0]
        assert form.instance.current_episode == current_episode[1]
        assert form.instance.next_season == next_episode[0]
        assert form.instance.next_episode == next_episode[1]

        update_next_air_date.assert_called_once_with()
