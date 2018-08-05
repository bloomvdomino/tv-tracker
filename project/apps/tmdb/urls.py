from rest_framework.routers import DefaultRouter

from .apps import TMDbConfig
from .views import ProgressViewSet

app_name = TMDbConfig.label

router = DefaultRouter()
router.register(r'progresses', ProgressViewSet, base_name='progress')

urlpatterns = router.urls
