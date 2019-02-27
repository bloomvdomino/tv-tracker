from django import forms

from .utils import search_show


class SearchForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        self.results = search_show(name)
        if not self.results:
            raise forms.ValidationError("No result found.")
        return name
