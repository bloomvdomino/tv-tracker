from datetime import date

import factory

from project.apps.accounts.tests.factories import UserFactory
from project.apps.tmdb.models import Progress


class ProgressFactory(factory.DjangoModelFactory):
    class Meta:
        model = Progress

    user = factory.SubFactory(UserFactory)

    show_id = 44217
    show_name = "Vikings"
    show_poster_path = "/94gP9uXNdbypwCLORjeurlad15Z.jpg"
    show_status = Progress.RETURNING

    next_air_date = date(2013, 3, 3)
