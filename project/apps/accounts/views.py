from django.contrib import messages
from django.contrib.auth import login, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import PasswordForm, SignupForm


class V2SignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('tmdb:v2_progresses')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class V2LoginView(views.LoginView):
    template_name = 'accounts/login.html'


class V2ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    fields = ['email']
    success_url = reverse_lazy('accounts:v2_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile saved.")
        return super().form_valid(form)


class V2PasswordView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/password.html'
    form_class = PasswordForm
    success_url = reverse_lazy('accounts:v2_login')

    def get_object(self, queryset=None):
        return self.request.user


class V2PasswordResetView(views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/emails/password_reset.html'
    subject_template_name = 'accounts/emails/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:v2_password_reset_done')


class V2PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class V2PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:v2_password_reset_complete')


class V2PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
