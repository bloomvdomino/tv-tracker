from django.urls import path

from .apps import TMDbConfig
from .views import (
    ProgressViewSet,
    V2PopularShowsView,
    V2ProgressesView,
    V2SearchView,
    V2ShowView,
)

app_name = TMDbConfig.label

urlpatterns = [
    path('progress/', ProgressViewSet.as_view({'post': 'create'}), name='progress'),
    path('progress/<int:show_id>/', ProgressViewSet.as_view({
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='progress-detail'),
    path('progress/list/', ProgressViewSet.as_view({'get': 'list'}), name='progress-list'),

    path('v2/popular_shows/', V2PopularShowsView.as_view(), name='v2_popular_shows'),
    path('v2/progresses/', V2ProgressesView.as_view(), name='v2_progresses'),
    path('v2/search/', V2SearchView.as_view(), name='v2_search'),
    path('v2/show/<int:id>/', V2ShowView.as_view(), name='v2_show'),
]
