from django.contrib.auth.views import LogoutView
from django.urls import path

from source.apps.accounts.apps import AccountsConfig
from source.apps.accounts.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    PasswordView,
    ProfileView,
    SignupView,
)

app_name = AccountsConfig.label

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/", PasswordView.as_view(), name="password"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password/reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("signup/", SignupView.as_view(), name="signup"),
]
