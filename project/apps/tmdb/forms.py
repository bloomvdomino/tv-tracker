from django import forms

from .utils import search_by_name


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        self.results = search_by_name(name)
        if not self.results:
            raise forms.ValidationError("No result found.")
        return name
