from django import forms

from source.apps.website.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "message"]
