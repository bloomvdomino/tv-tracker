from rest_framework.routers import DefaultRouter

from .views import ProgressViewSet

app_name = 'apps_accounts'

router = DefaultRouter()
router.register(r'progresses', ProgressViewSet, base_name='progress')

urlpatterns = router.urls
