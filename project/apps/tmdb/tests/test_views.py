import pytest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from ..views import ProgressDeleteView, ProgressEditMixin, ProgressUpdateView, WatchNextView
from .factories import ProgressFactory


class TestWatchNextView:
    def test_login_required(self):
        assert issubclass(WatchNextView, LoginRequiredMixin)

    @pytest.mark.django_db
    def test_post(self, mocker, client):
        update_show_data = mocker.patch("project.apps.tmdb.models.Progress.update_show_data")
        watch_next = mocker.patch("project.apps.tmdb.models.Progress.watch_next")
        progress = ProgressFactory()
        client.login(username=progress.user.email, password="123123")
        url = reverse("tmdb:watch_next", kwargs={"show_id": progress.show_id})

        response = client.patch(url, content_type="application/json")

        assert response.status_code == 200
        update_show_data.assert_called_once_with()
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


class TestProgressEditMixin:
    @pytest.fixture
    def dummy_view_class(self):
        class Base:
            def get_context_data(self, **kwargs):
                return {"context_data": 123}

            def get_form_kwargs(self):
                return {"form_kwarg": 123}

        class Dummy(ProgressEditMixin, Base):
            pass

        return Dummy

    def test_get_context_data(self, mocker, dummy_view_class):
        view = dummy_view_class()
        view.show = mocker.MagicMock()

        context_data = view.get_context_data()

        assert len(context_data) == 2
        assert context_data["context_data"] == 123
        assert context_data["show"] == view.show

    def test_get_form_kwargs(self, mocker, dummy_view_class):
        view = dummy_view_class()
        view.request = mocker.MagicMock()
        view.show = mocker.MagicMock()

        form_kwargs = view.get_form_kwargs()

        assert len(form_kwargs) == 3
        assert form_kwargs["form_kwarg"] == 123
        assert form_kwargs["user"] == view.request.user
        assert form_kwargs["show"] == view.show


class TestProgressUpdateView:
    def test_get_initial(self, mocker):
        show = mocker.MagicMock()
        mocker.patch(
            "project.apps.tmdb.views.ProgressEditMixin.show",
            new=mocker.PropertyMock(return_value=show),
        )

        view = ProgressUpdateView()
        view.object = ProgressFactory.build()

        initial = view.get_initial()

        assert len(initial) == 2
        assert initial["status"] == view.object.status
        assert initial["last_watched"] == "0-0"
