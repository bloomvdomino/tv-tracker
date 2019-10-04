from django import forms

from project.apps.website.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["email", "message"]
