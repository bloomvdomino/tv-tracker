import pytest

from project.apps.accounts.forms import SignupForm
from project.apps.accounts.models import User


class TestSignupForm:
    @pytest.mark.django_db
    def test_save(self):
        data = {
            "email": "u1@tt.com",
            "password": "foobar123!",
            "time_zone": User.TZ_AMERICA_NEW_YORK,
        }
        form = SignupForm()
        form.cleaned_data = data

        user = form.save()

        assert user.email == data["email"]
        assert user.check_password(data["password"])
        assert user.time_zone == data["time_zone"]
