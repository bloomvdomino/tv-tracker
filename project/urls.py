from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import include, path

admin.site.unregister(Group)

urlpatterns = [
    path('', include('project.apps.website.urls', namespace='website')),
    path('accounts/', include('project.apps.accounts.urls', namespace='accounts')),
    path('tmdb/', include('project.apps.tmdb.urls', namespace='tmdb')),

    path(settings.ADMIN_PATH, admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
