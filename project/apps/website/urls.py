from django.urls import path

from .apps import WebsiteConfig
from .views import IndexView, V2ContactView

app_name = WebsiteConfig.label

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('v2/contact/', V2ContactView.as_view(), name='v2_contact'),
]
