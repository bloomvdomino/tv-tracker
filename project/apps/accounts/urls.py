from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from .apps import AccountsConfig
from .views import EmailView, PasswordView, ProfileView, SignupView

app_name = AccountsConfig.label

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', ObtainJSONWebToken.as_view(), name='login'),
    path('refresh-token/', RefreshJSONWebToken.as_view(), name='refresh-token'),
    path('email/', EmailView.as_view(), name='email'),
    path('password/', PasswordView.as_view(), name='password'),
    path('profile/', ProfileView.as_view(), name='profile')
]
