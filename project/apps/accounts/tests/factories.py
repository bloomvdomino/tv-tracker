import factory

from ..models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = "u1@tt.com"
