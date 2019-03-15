import pytest

from ..utils import format_episode_label


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
