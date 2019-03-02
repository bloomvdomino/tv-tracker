from django import forms

from .models import Progress
from .utils import search_show


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
            'is_followed',
            'show_id',
            'show_name',
            'show_poster_path',
            'show_status',
        ]

    def __init__(self, *args, **kwargs):
        self.show = kwargs.pop('show')
        super().__init__(*args, **kwargs)
        self.fields['last_watched'].choices = self.make_episode_choices(self.show['seasons'])

    def clean_last_watched(self):
        last_watched = self.cleaned_data['last_watched']
        last_watched_season, last_watched_episode = map(int, last_watched.split('-'))

        last_aired = self.show.get('last_episode_to_air', {})
        last_aired_season = last_aired.get('season_number', 0)
        last_aired_episode = last_aired.get('episode_number', 0)

        if last_watched_season > last_aired_season or last_watched_episode > last_aired_episode:
            raise forms.ValidationError("This episode is not available, yet.")

        self.cleaned_data.update(
            current_season=last_watched_season,
            current_episode=last_watched_episode,
        )

        return last_watched

    def save(self, commit=True):
        if self.cleaned_data.get('delete', False):
            self.instance.delete()
            return None

        self.instance.current_season = self.cleaned_data['current_season']
        self.instance.current_episode = self.cleaned_data['current_episode']
        return super().save(commit=commit)

    @staticmethod
    def make_episode_choices(seasons):
        episode_choices = [('0-0', "Not started, yet.")]
        for season, info in enumerate(seasons, 1):
            for episode in range(1, info['episode_count'] + 1):
                value = '{}-{}'.format(season, episode)
                season_label = '0{}'.format(season)[-2:]
                episode_label = '0{}'.format(episode)[-2:]
                label = "S{}E{}".format(season_label, episode_label)
                episode_choices.append((value, label))
        return episode_choices


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        self.results = search_show(name)
        if not self.results:
            raise forms.ValidationError("No result found.")
        return name
