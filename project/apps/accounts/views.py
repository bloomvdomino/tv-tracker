from django.contrib import messages
from django.contrib.auth import login, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from project.apps.accounts.forms import PasswordForm, SignupForm


class SignupView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("tmdb:progresses")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class LoginView(views.LoginView):
    template_name = "accounts/login.html"


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    fields = ["email", "time_zone"]
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile saved.")
        return super().form_valid(form)


class PasswordView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/password.html"
    form_class = PasswordForm
    success_url = reverse_lazy("accounts:login")

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(views.PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/emails/password_reset.html"
    subject_template_name = "accounts/emails/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
