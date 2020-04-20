import factory

from source.apps.accounts.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = "u1@tt.com"
    password = factory.PostGenerationMethodCall("set_password", "123123")
