from django import forms

from .models import Progress
from .utils import format_episode_label, search_show


class ProgressForm(forms.ModelForm):
    last_watched = forms.ChoiceField()

    class Meta:
        model = Progress
        fields = ["status"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.show = kwargs.pop("show")
        self.updating = kwargs.get("instance") is not None

        super().__init__(*args, **kwargs)

        if self.updating:
            self.instance.update_show_data()

        self.fields["last_watched"].choices = self._make_episode_choices()

    def _make_episode_choices(self):
        episode_choices = [("0-0", "Not started, yet.")]
        for season, episode in self.show.aired_episodes:
            value = "{}-{}".format(season, episode)
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
        self.instance.update_next_air_date()

        return last_watched

    def save(self, commit=True):
        self.instance.user = self.user
        self.instance.show_id = self.show.id
        super().save(commit=commit)

        if not self.updating:
            self.instance.update_show_data()

        return self.instance


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
