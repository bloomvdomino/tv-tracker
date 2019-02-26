from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from rest_framework import mixins, viewsets

from .forms import SearchForm
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


class V2ProgressesView(LoginRequiredMixin, TemplateView):
    template_name = 'tmdb/progresses.html'


class V2PopularShowsView(TemplateView):
    template_name = 'tmdb/popular_shows.html'


class V2SearchView(FormView):
    template_name = 'tmdb/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)
