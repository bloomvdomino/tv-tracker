from django.urls import path

from .apps import WebsiteConfig
from .views import ContactView, IndexView

app_name = WebsiteConfig.label

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
]
