from django.urls import path

from project.core.apps import CoreConfig
from project.core.views import HealthCheckView

app_name = CoreConfig.label

urlpatterns = [path("health/", HealthCheckView.as_view(), name="health_check")]
