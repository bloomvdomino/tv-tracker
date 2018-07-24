from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import include, path

admin.site.unregister(Group)

urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),

    path('accounts/', include('project.apps.accounts.urls', namespace='accounts')),
    path('tmdb/', include('project.apps.tmdb.urls', namespace='tmdb'))
]
