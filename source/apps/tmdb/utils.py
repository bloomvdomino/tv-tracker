import httpx
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property


class Show:
    def __init__(self, data, user=None):
        self._data = data
        self._set_progress_related(user)

    @property
    def id(self):
        return self._data["id"]

    @property
    def name(self):
        return self._data["name"]

    @property
    def poster_path(self):
        # Return empty string instead of None to avoid violating not-null constraint.
        return self._data["poster_path"] or ""

    @property
    def vote_average(self):
        return self._data["vote_average"]

    @property
    def genres(self):
        return [genre["name"] for genre in self._data["genres"]]

    @property
    def languages(self):
        return self._data["languages"]

    @property
    def overview(self):
        return self._data["overview"]

    @property
    def status_display(self):
        return self._data["status"]

    @cached_property
    def status_value(self):
        from source.apps.tmdb.models import Progress  # imported here to avoid circular dependency

        value_display_map = dict(Progress.SHOW_STATUS_CHOICES)
        display_value_map = {display: value for value, display in value_display_map.items()}
        return display_value_map[self.status_display]

    @cached_property
    def aired_episodes(self):
        aired_episodes = []
        for season, season_data in enumerate(self._seasons, 1):
            for episode in range(1, season_data["episode_count"] + 1):
                if not self._episode_aired(season, episode):
                    break
                aired_episodes.append((season, episode))
        return aired_episodes

    def _episode_aired(self, season, episode):
        last_aired_season, last_aired_episode = self.last_aired_episode
        if not (last_aired_season and last_aired_episode):
            return False
        return not (
            season > last_aired_season
            or (season == last_aired_season and episode > last_aired_episode)
        )

    @cached_property
    def last_aired_episode(self):
        last_aired = self._data["last_episode_to_air"]
        if not last_aired:
            return None, None
        return last_aired["season_number"], last_aired["episode_number"]

    def get_next_episode(self, season, episode):
        if not (season and episode):
            return 1, 1
        if episode < self._seasons[season - 1]["episode_count"]:
            # Not the last episode in the season.
            return season, episode + 1
        if season < len(self._seasons):
            # Not the last seasons.
            return season + 1, 1
        return None, None

    @cached_property
    def _seasons(self):
        """
        Return only non-special and non-empty seasons of the show.

        TMDb API may return some especial seasons as the first element in the
        list. And the last season may be empty.
        """
        seasons = self._data["seasons"]
        if seasons[0]["season_number"] == 0:
            del seasons[0]
        if not seasons[-1]:
            del seasons[-1]
        return seasons

    def _set_progress_related(self, user):
        self.saved = False
        if user and user.is_authenticated:
            self.saved = user.progress_set.filter(show_id=self.id).exists()
        action = "update" if self.saved else "create"
        self.edit_url = reverse(f"tmdb:progress_{action}", kwargs={"show_id": self.id})


def format_episode_label(season, episode):
    season = f"0{season}"[-2:] if season < 100 else season
    episode = f"0{episode}"[-2:] if episode < 100 else episode
    return f"S{season}E{episode}"


def fetch(endpoint, params=None):
    if not settings.TMDB_API_KEY:
        raise Exception("TMDB_API_KEY not provided.")

    url = f"{settings.TMDB_API_URL}/{endpoint}"
    params = params or {}
    params.update(api_key=settings.TMDB_API_KEY)
    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_show(show_id, user=None):
    """
    Get a TV show detail by ID.

    https://developers.themoviedb.org/3/tv/get-tv-details
    """
    data = fetch(f"tv/{show_id}")
    return Show(data, user=user)


def get_air_date(show_id, season, episode):
    endpoint = f"tv/{show_id}/season/{season}/episode/{episode}"

    # air_date from response data can be empty string, we want to return None in
    # this case as well.
    return fetch(endpoint).get("air_date") or None


def get_popular_shows(page, user=None):
    """
    Get popular TV shows by page.

    https://developers.themoviedb.org/3/tv/get-popular-tv-shows
    """
    results = fetch("tv/popular", params={"page": page})["results"]
    return [Show(data, user=user) for data in results]


def search_show(name, user=None):
    """
    Search for TV shows by name.

    https://developers.themoviedb.org/3/search/search-tv-shows
    """
    results = fetch("search/tv", params={"query": name})["results"]
    return [Show(data, user=user) for data in results]
