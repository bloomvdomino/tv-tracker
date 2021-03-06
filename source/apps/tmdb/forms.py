from itertools import chain

from django import forms

from source.apps.tmdb.models import Progress
from source.apps.tmdb.utils import format_episode_label, search_show


class FilterForm(forms.Form):
    genre = forms.ChoiceField(required=False)
    language = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")

        super().__init__(*args, **kwargs)

        self.fields["genre"].choices = self._make_genre_choices()
        self.fields["language"].choices = self._make_language_choices()

    def _make_genre_choices(self):
        genres = self.user.progress_set.values_list("show_genres", flat=True)
        return [("", "-")] + [(genre, genre) for genre in sorted(set(chain(*genres)))]

    def _make_language_choices(self):
        languages = self.user.progress_set.values_list("show_languages", flat=True)
        return [("", "-")] + [
            (langauge, langauge.upper()) for langauge in sorted(set(chain(*languages)))
        ]


class ProgressForm(forms.ModelForm):
    last_watched = forms.ChoiceField()

    class Meta:
        model = Progress
        fields = [
            "status",
            "show_id",
            "show_name",
            "show_poster_path",
            "show_status",
            "show_genres",
            "show_languages",
            "last_aired_season",
            "last_aired_episode",
        ]

    def __init__(self, *args, **kwargs):
        self.show = kwargs.pop("show")
        super().__init__(*args, **kwargs)
        self.fields["last_watched"].choices = self._make_episode_choices()

    def _make_episode_choices(self):
        episode_choices = [("0-0", "Not started, yet.")]
        for season, episode in self.show.aired_episodes:
            value = f"{season}-{episode}"
            label = format_episode_label(season, episode)
            episode_choices.append((value, label))
        return episode_choices

    def clean_last_watched(self):
        last_watched = self.cleaned_data["last_watched"]

        self.instance.current_season, self.instance.current_episode = map(
            int, last_watched.split("-")
        )
        self.instance.next_season, self.instance.next_episode = self.show.get_next_episode(
            self.instance.current_season, self.instance.current_episode
        )

        return last_watched


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"autofocus": "autofocus"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data["name"]
        self.results = search_show(name, user=self.user)
        if not self.results:
            raise forms.ValidationError("No result found.")
        return name
