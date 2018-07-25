from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken

from .views import EmailView, PasswordView, SignupView

app_name = 'apps_accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', ObtainJSONWebToken.as_view(), name='login'),
    path('refresh-token/', RefreshJSONWebToken.as_view(), name='refresh-token'),
    path('email/', EmailView.as_view(), name='email'),
    path('password/', PasswordView.as_view(), name='password')
]
