from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import EmailView, PasswordView, SignupView

app_name = 'apps_accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh-token/', refresh_jwt_token, name='refresh-token'),
    path('email/', EmailView.as_view(), name='email'),
    path('password/', PasswordView.as_view(), name='password')
]
