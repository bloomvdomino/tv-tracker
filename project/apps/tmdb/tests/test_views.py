import pytest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from ..views import ProgressDeleteView, WatchNextView
from .factories import ProgressFactory


class TestWatchNextView:
    def test_login_required(self):
        assert issubclass(WatchNextView, LoginRequiredMixin)

    @pytest.mark.django_db
    def test_post(self, mocker, client):
        watch_next = mocker.patch("project.apps.tmdb.models.Progress.watch_next")
        progress = ProgressFactory()
        client.login(username=progress.user.email, password="123123")
        url = reverse("tmdb:watch_next", kwargs={"show_id": progress.show_id})

        response = client.patch(url, content_type="application/json")

        assert response.status_code == 200
        watch_next.assert_called_once_with()


class TestProgressDeleteView:
    def test_login_required(self):
        assert issubclass(ProgressDeleteView, LoginRequiredMixin)

    @pytest.mark.django_db
    def test_patch(self, client):
        progress = ProgressFactory()
        user = progress.user
        client.login(username=user.email, password="123123")
        url = reverse("tmdb:progress_delete", kwargs={"show_id": progress.show_id})

        response = client.delete(url, content_type="application/json")

        assert response.status_code == 200
        assert user.progress_set.count() == 0
