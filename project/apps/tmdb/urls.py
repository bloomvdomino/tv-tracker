from django.urls import path

from .apps import TMDbConfig
from .views import (
    V2PopularShowsView,
    V2ProgressCreateView,
    V2ProgressesView,
    V2ProgressUpdateView,
    V2SearchView,
    V2ShowView,
)

app_name = TMDbConfig.label

urlpatterns = [
    path('v2/popular_shows/', V2PopularShowsView.as_view(), name='v2_popular_shows'),
    path('v2/progresses/', V2ProgressesView.as_view(), name='v2_progresses'),
    path('v2/search/', V2SearchView.as_view(), name='v2_search'),
    path('v2/show/<int:id>/', V2ShowView.as_view(), name='v2_show'),
    path('v2/show/<int:show_id>/progress/create/', V2ProgressCreateView.as_view(), name='v2_progress_create'),
    path('v2/show/<int:show_id>/progress/update/', V2ProgressUpdateView.as_view(), name='v2_progress_update'),
]
