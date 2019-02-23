from django.urls import path

from .apps import TMDbConfig
from .views import ProgressViewSet

app_name = TMDbConfig.label

urlpatterns = [
    path('progress/', ProgressViewSet.as_view({'post': 'create'}), name='progress'),
    path('progress/<int:show_id>/', ProgressViewSet.as_view({
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='progress-detail'),
    path('progress/list/', ProgressViewSet.as_view({'get': 'list'}), name='progress-list'),
]
