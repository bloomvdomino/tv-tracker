from django import forms

from .models import Progress
from .utils import search_show


class ProgressForm(forms.ModelForm):
    show_id = forms.IntegerField(widget=forms.HiddenInput())
    show_name = forms.CharField(widget=forms.HiddenInput())
    show_poster_path = forms.CharField(widget=forms.HiddenInput())
    show_status = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Progress
        fields = [
            'is_followed',
            'show_id',
            'show_name',
            'show_poster_path',
            'show_status',
        ]


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        self.results = search_show(name)
        if not self.results:
            raise forms.ValidationError("No result found.")
        return name
