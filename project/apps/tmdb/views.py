from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from .models import Progress
from .serializers import ProgressSerializer


class ProgressViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ProgressSerializer
    lookup_field = 'show_id'

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)


class V2ProgressesView(TemplateView):
    template_name = 'tmdb/progresses.html'


class V2PopularShowsView(TemplateView):
    template_name = 'tmdb/popular_shows.html'


class V2SearchView(TemplateView):
    template_name = 'tmdb/search.html'
