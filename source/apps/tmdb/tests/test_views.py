import pytest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from source.apps.accounts.tests.factories import UserFactory
from source.apps.tmdb.tests.factories import ProgressFactory
from source.apps.tmdb.views import (
    ProgressCreateView,
    ProgressDeleteView,
    ProgressEditMixin,
    ProgressUpdateView,
    WatchNextView,
)


class TestWatchNextView:
    def test_login_required(self):
        assert issubclass(WatchNextView, LoginRequiredMixin)

    @pytest.mark.django_db
    def test_post(self, mocker, client):
        progress = ProgressFactory()
        client.login(username=progress.user.email, password="123123")
        url = reverse("tmdb:watch_next", kwargs={"show_id": progress.show_id})

        update_show_data = mocker.patch("source.apps.tmdb.models.Progress.update_show_data")
        watch_next = mocker.patch("source.apps.tmdb.models.Progress.watch_next")
        stop_if_finished = mocker.patch("source.apps.tmdb.models.Progress.stop_if_finished")
        save = mocker.patch("source.apps.tmdb.models.Progress.save")

        response = client.patch(url, content_type="application/json")

        assert response.status_code == 200
        update_show_data.assert_called_once_with()
        watch_next.assert_called_once_with()
        stop_if_finished.assert_called_once_with()
        save.assert_called_once_with()


@pytest.mark.django_db
class TestProgressesView:
    @pytest.fixture
    def url(self):
        return reverse("tmdb:progresses")

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def auth_client(self, client, user):
        client.login(username=user.email, password="123123")
        return client

    @pytest.mark.parametrize("method", ["get", "post"])
    def test_get_and_post_without_filter(self, url, user, auth_client, method):
        p1 = ProgressFactory(user=user, show_id=1, show_name="Vikings", show_languages=["en"])
        p2 = ProgressFactory(
            user=user, show_id=2, show_name="Itaewon Class", show_languages=["ko", "en"]
        )

        response = getattr(auth_client, method)(url)

        assert response.status_code == 200
        available = response.context["available"]
        assert len(available) == 2
        assert p1 in available
        assert p2 in available

    def test_post_with_filter(self, url, user, auth_client):
        ProgressFactory(user=user, show_id=1, show_name="Vikings", show_languages=["en"])
        p2 = ProgressFactory(
            user=user, show_id=2, show_name="Itaewon Class", show_languages=["ko", "en"]
        )

        response = auth_client.post(url, data={"language": "ko"})

        assert response.status_code == 200
        available = response.context["available"]
        assert len(available) == 1
        assert p2 in available


class TestProgressEditMixin:
    @pytest.fixture
    def dummy_view_class(self):
        class Base:
            def get_context_data(self, **kwargs):
                return {"context_data": 123}

            def get_form_kwargs(self):
                return {"form_kwarg": 123}

            def get_initial(self):
                return {"initial": 123}

            def form_valid(self, form):
                return True

        class Dummy(ProgressEditMixin, Base):
            pass

        return Dummy

    def test_show(self, mocker):
        show = mocker.MagicMock()
        get_show = mocker.patch("source.apps.tmdb.views.get_show", return_value=show)

        mixin = ProgressEditMixin()
        mixin.kwargs = {"show_id": 1}
        mixin.request = mocker.MagicMock()

        assert mixin.show == show
        get_show.assert_called_once_with(1, user=mixin.request.user)

        assert mixin.show == show
        assert get_show.call_count == 1

    @pytest.mark.django_db
    def test_get_object_with_authenticated_user(self, mocker):
        user = UserFactory()
        progress = ProgressFactory(user=user)

        mixin = ProgressEditMixin()
        mixin.request = mocker.MagicMock(user=user)
        mixin.show = mocker.MagicMock(id=progress.show_id)

        assert mixin.get_object() == progress

    def test_get_object_with_anonymous_user(self, mocker):
        user = AnonymousUser()
        mixin = ProgressEditMixin()
        mixin.request = mocker.MagicMock(user=user)

        assert mixin.get_object() is None

    def test_get_context_data(self, mocker, dummy_view_class):
        view = dummy_view_class()
        view.show = mocker.MagicMock()

        context_data = view.get_context_data()

        assert len(context_data) == 2
        assert context_data["context_data"] == 123
        assert context_data["show"] == view.show

    def test_get_form_kwargs(self, mocker, dummy_view_class):
        view = dummy_view_class()
        view.show = mocker.MagicMock()

        form_kwargs = view.get_form_kwargs()

        assert len(form_kwargs) == 2
        assert form_kwargs["form_kwarg"] == 123
        assert form_kwargs["show"] == view.show

    def test_get_initial(self, mocker, dummy_view_class):
        view = dummy_view_class()
        view.show = mocker.MagicMock(last_aired_episode=(4, 5))

        initial = view.get_initial()

        assert len(initial) == 8
        assert initial["initial"] == 123
        assert initial["show_id"] == view.show.id
        assert initial["show_name"] == view.show.name
        assert initial["show_poster_path"] == view.show.poster_path
        assert initial["show_status"] == view.show.status_value
        assert initial["show_languages"] == view.show.languages
        assert initial["last_aired_season"] == 4
        assert initial["last_aired_episode"] == 5

    def test_form_valid(self, mocker, dummy_view_class):
        progress = mocker.MagicMock()
        form = mocker.MagicMock(instance=progress)
        view = dummy_view_class()

        assert view.form_valid(form)

        progress.update_next_air_date.assert_called_once_with()
        progress.stop_if_finished.assert_called_once_with()


class TestProgressCreateView:
    def test_form_valid(self, mocker):
        super_form_valid = mocker.patch(
            "source.apps.tmdb.views.CreateView.form_valid", return_value=True
        )

        user = UserFactory.build()
        form = mocker.MagicMock()

        view = ProgressCreateView()
        view.request = mocker.MagicMock(user=user)

        assert view.form_valid(form)

        assert form.instance.user == user
        super_form_valid.assert_called_once_with(form)


class TestProgressUpdateView:
    def test_get_initial(self, mocker):
        mocker.patch(
            "source.apps.tmdb.views.ProgressEditMixin.get_initial", return_value={"initial": 123}
        )

        view = ProgressUpdateView()
        view.object = ProgressFactory.build()

        initial = view.get_initial()

        assert len(initial) == 3
        assert initial["initial"] == 123
        assert initial["status"] == view.object.status
        assert initial["last_watched"] == "0-0"


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
