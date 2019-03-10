from django import forms

from .models import Progress
from .utils import (
    format_episode_label,
    get_air_date,
    get_aired_episodes,
    get_next_episode,
    search_show,
)


class ProgressForm(forms.ModelForm):
    show_id = forms.IntegerField(widget=forms.HiddenInput())
    show_name = forms.CharField(widget=forms.HiddenInput())
    show_poster_path = forms.CharField(widget=forms.HiddenInput())
    show_status = forms.CharField(widget=forms.HiddenInput())

    last_watched = forms.ChoiceField()

    delete = forms.BooleanField(required=False)

    class Meta:
        model = Progress
        fields = [
            'status',
            'show_id',
            'show_name',
            'show_poster_path',
            'show_status',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.show = kwargs.pop('show')
        super().__init__(*args, **kwargs)
        self.fields['last_watched'].choices = self._make_episode_choices()

    def clean_last_watched(self):
        last_watched = self.cleaned_data['last_watched']
        season, episode = map(int, last_watched.split('-'))
        self.cleaned_data.update(current_season=season, current_episode=episode)
        return last_watched

    def clean_status(self):
        status = self.cleaned_data['status']
        if status == Progress.FOLLOWING:
            following = self.user.progress_set.filter(status=status).exclude(show_id=self.show['id']).count()
            limit = self.user.max_following_shows
            if following >= limit:
                message = "You cannot follow more than {} shows.".format(limit)
                raise forms.ValidationError(message)
        return status

    def save(self, commit=True):
        if self.cleaned_data.get('delete', False):
            self.instance.delete()
            return None

        self._update_episodes()
        self.instance.user = self.user
        return super().save(commit=commit)

    def _make_episode_choices(self):
        episode_choices = [('0-0', "Not started, yet.")]
        for season, episode in get_aired_episodes(self.show):
            value = '{}-{}'.format(season, episode)
            label = format_episode_label(season, episode)
            episode_choices.append((value, label))
        return episode_choices

    def _update_episodes(self):
        current_season = self.cleaned_data['current_season']
        current_episode = self.cleaned_data['current_episode']

        if self.instance.current_season == current_season and self.instance.current_episode == current_episode:
            return

        self.instance.current_season = current_season
        self.instance.current_episode = current_episode
        self.instance.next_season, self.instance.next_episode = get_next_episode(
            self.show,
            current_season,
            current_episode,
        )

        if not (self.instance.next_season and self.instance.next_episode):
            self.instance.next_air_date = None
            return

        self.instance.next_air_date = get_air_date(
            self.instance.show_id,
            self.instance.next_season,
            self.instance.next_episode,
        )


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        self.results = search_show(name)
        if not self.results:
            raise forms.ValidationError("No result found.")
        return name
