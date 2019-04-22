from datetime import date

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
    def get_air_date(self, mocker):
        return mocker.patch("project.apps.tmdb.forms.get_air_date", return_value=date(2013, 3, 3))

    @pytest.mark.parametrize(
        "current_episode,next_episode,next_air_date",
        [
            ((0, 0), (None, None), None),
            ((0, 0), (1, None), None),
            ((0, 0), (None, 1), None),
            ((0, 0), (1, 1), date(2013, 3, 3)),
            ((1, 1), (None, None), None),
            ((1, 1), (1, None), None),
            ((1, 1), (None, 1), None),
            ((1, 1), (1, 2), date(2013, 3, 3)),
        ],
    )
    def test_update_episodes(
        self, instance, show, get_air_date, current_episode, next_episode, next_air_date
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
        assert form.instance.next_air_date == next_air_date
