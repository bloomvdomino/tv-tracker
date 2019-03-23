from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import User


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update(widget=forms.PasswordInput())
        super().__init__(*args, **kwargs)
        self.validators.append(validate_password)


class PasswordConfirmMixin(forms.Form):
    password_confirm = PasswordField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Incorrect new password confirmation.")
        return cleaned_data


class SignupForm(PasswordConfirmMixin, forms.ModelForm):
    password = PasswordField()

    class Meta:
        model = User
        fields = ['email', 'password', 'time_zone']

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        time_zone = self.cleaned_data['time_zone']
        self.instance = User.objects.create_user(email, password, time_zone=time_zone)
        return self.instance


class PasswordForm(PasswordConfirmMixin, forms.ModelForm):
    current_password = PasswordField()
    password = PasswordField()

    class Meta:
        model = User
        fields = ['password']

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Incorrect current password.")
        return current_password

    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data['password'])
        self.instance.save()
        return self.instance
