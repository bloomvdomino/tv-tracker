import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from project.apps.accounts.tests.factories import UserFactory
from project.apps.website.views import ContactView


class TestIndexView:
    def test_anonymous_user(self, client):
        response = client.get(reverse("website:index"))

        assert response.status_code == 302
        assert response["Location"] == "/popular_shows/"

    @pytest.mark.django_db
    def test_authenticated_user(self, client):
        user = UserFactory()
        client.login(username=user.email, password="123123")

        response = client.get(reverse("website:index"))

        assert response.status_code == 302
        assert response["Location"] == "/progresses/"


class TestContactView:
    def test_get_initial_anonymous_user(self, mocker):
        view = ContactView()
        view.request = mocker.MagicMock(user=AnonymousUser())

        initial = view.get_initial()

        assert initial == {}

    @pytest.mark.django_db
    def test_get_initial_authenticated_user(self, mocker):
        user = UserFactory()

        view = ContactView()
        view.request = mocker.MagicMock(user=user)

        initial = view.get_initial()

        assert initial == {"email": user.email}

    def test_form_valid_anonymous_user(self, mocker):
        success = mocker.patch("project.apps.website.views.messages.success")
        form = mocker.MagicMock(instance=mocker.MagicMock(user=None))

        view = ContactView()
        view.request = mocker.MagicMock(user=AnonymousUser())

        view.form_valid(form)

        assert form.instance.user is None
        success.assert_called_once_with(
            view.request, "Your message has been sent, thank you for contacting us."
        )

    @pytest.mark.django_db
    def test_form_valid_authenticated_user(self, mocker):
        success = mocker.patch("project.apps.website.views.messages.success")
        user = UserFactory()
        form = mocker.MagicMock(instance=mocker.MagicMock(user=user))

        view = ContactView()
        view.request = mocker.MagicMock(user=user)

        view.form_valid(form)

        assert form.instance.user == user
        success.assert_called_once_with(
            view.request, "Your message has been sent, thank you for contacting us."
        )
