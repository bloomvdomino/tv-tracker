import pytest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from ..views import WatchNextView
from .factories import ProgressFactory


class TestWatchNextView:
    def test_login_required(self):
        assert issubclass(WatchNextView, LoginRequiredMixin)

    def test_allowed_methods(self):
        assert WatchNextView.http_method_names == ["patch"]

    @pytest.mark.django_db
    def test_post(self, mocker, client):
        watch_next = mocker.patch("project.apps.tmdb.models.Progress.watch_next")
        progress = ProgressFactory()
        client.login(username=progress.user.email, password="123123")
        url = reverse("tmdb:watch_next", kwargs={"show_id": progress.show_id})

        response = client.patch(url, content_type="application/json")

        assert response.status_code == 200
        watch_next.assert_called_once_with()
