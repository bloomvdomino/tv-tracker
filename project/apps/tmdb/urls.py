from django.urls import path

from .apps import TMDbConfig
from .views import (
    PopularShowsView,
    ProgressCreateView,
    ProgressesView,
    ProgressUpdateView,
    SearchView,
    WatchNextView,
)

app_name = TMDbConfig.label

urlpatterns = [
    path("popular_shows/", PopularShowsView.as_view(), name="popular_shows"),
    path("progress/watch_next/<int:show_id>/", WatchNextView.as_view(), name="watch_next"),
    path("progresses/", ProgressesView.as_view(), name="progresses"),
    path("search/", SearchView.as_view(), name="search"),
    path(
        "show/<int:show_id>/progress/create/", ProgressCreateView.as_view(), name="progress_create"
    ),
    path(
        "show/<int:show_id>/progress/update/", ProgressUpdateView.as_view(), name="progress_update"
    ),
]
