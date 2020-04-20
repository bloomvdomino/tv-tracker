import pytest

from source.apps.accounts.managers import UserManager
from source.apps.accounts.models import User


class TestUserManager:
    @pytest.fixture
    def manager(self):
        return UserManager()

    @pytest.fixture
    def create_user(self, mocker):
        return mocker.patch("source.apps.accounts.managers.UserManager._create_user")

    @pytest.mark.django_db
    def test__create_user(self):
        user = User.objects._create_user("u@test.com", "123", is_staff=False, is_superuser=True)

        assert user.email == "u@test.com"
        assert user.check_password("123")
        assert not user.is_staff
        assert user.is_superuser

    def test_create_user(self, manager, create_user):
        manager.create_user("u@test.com", "123", is_staff=True, is_superuser=True, foo=123)
        create_user.assert_called_once_with(
            "u@test.com", "123", is_staff=False, is_superuser=False, foo=123
        )

    def test_create_superuser(self, manager, create_user):
        manager.create_superuser("u@test.com", "123", is_staff=False, is_superuser=False, foo=123)
        create_user.assert_called_once_with(
            "u@test.com", "123", is_staff=True, is_superuser=True, foo=123
        )
