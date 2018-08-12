from django.urls import path

from .apps import WebsiteConfig
from .views import ContactView

app_name = WebsiteConfig.label

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact')
]
