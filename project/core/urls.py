from django.urls import path

from .apps import CoreConfig
from .views import HealthCheckView

app_name = CoreConfig.label

urlpatterns = [path("health/", HealthCheckView.as_view(), name="health_check")]
