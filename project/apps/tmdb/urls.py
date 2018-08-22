from rest_framework.routers import SimpleRouter

from .apps import TMDbConfig
from .views import ProgressViewSet

app_name = TMDbConfig.label

router = SimpleRouter()
router.register(r'progresses', ProgressViewSet, base_name='progress')

urlpatterns = router.urls
