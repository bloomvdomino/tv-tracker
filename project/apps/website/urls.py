from django.urls import path

from .apps import WebsiteConfig
from .views import ContactView, V2ContactView

app_name = WebsiteConfig.label

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),

    path('v2/contact/', V2ContactView.as_view(), name='v2_contact'),
]
