from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from .apps import AccountsConfig
from .views import (
    EmailView,
    PasswordResetTokenView,
    PasswordResetView,
    PasswordView,
    ProfileView,
    SignupView,
    V2LoginView,
    V2PasswordResetCompleteView,
    V2PasswordResetConfirmView,
    V2PasswordResetDoneView,
    V2PasswordResetView,
    V2PasswordView,
    V2ProfileView,
    V2SignupView,
)

app_name = AccountsConfig.label

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', ObtainJSONWebToken.as_view(), name='login'),
    path('refresh-token/', RefreshJSONWebToken.as_view(), name='refresh-token'),
    path('email/', EmailView.as_view(), name='email'),
    path('password/', PasswordView.as_view(), name='password'),
    path('password/reset/', PasswordResetTokenView.as_view(), name='password-reset-token'),
    path('password/reset/<uuid:pk>/', PasswordResetView.as_view(), name='password-reset'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('v2/login/', V2LoginView.as_view(), name='v2_login'),
    path('v2/logout/', LogoutView.as_view(), name='v2_logout'),
    path('v2/password/', V2PasswordView.as_view(), name='v2_password'),
    path('v2/password/reset/', V2PasswordResetView.as_view(), name='v2_password_reset'),
    path('v2/password/reset/complete/', V2PasswordResetCompleteView.as_view(), name='v2_password_reset_complete'),
    path(
        'v2/password/reset/confirm/<uidb64>/<token>/',
        V2PasswordResetConfirmView.as_view(),
        name='v2_password_reset_confirm',
    ),
    path('v2/password/reset/done/', V2PasswordResetDoneView.as_view(), name='v2_password_reset_done'),
    path('v2/profile/', V2ProfileView.as_view(), name='v2_profile'),
    path('v2/signup/', V2SignupView.as_view(), name='v2_signup'),
]
