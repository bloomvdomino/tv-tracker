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
]
