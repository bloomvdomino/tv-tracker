from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from rest_framework import mixins, viewsets

from .forms import SearchForm
from .models import Progress
from .serializers import ProgressSerializer
from .utils import get_popular_shows, get_show


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

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        min_page = 1
        max_page = 1000

        page = int(self.request.GET.get('page', min_page))
        page = page if page >= min_page else min_page
        page = page if page <= max_page else max_page
        kwargs.update(current_page=page, shows=get_popular_shows(page))

        if page - 1 >= min_page:
            kwargs.update(previous_page_link=self.make_page_link(page - 1))

        if page + 1 <= max_page:
            kwargs.update(next_page_link=self.make_page_link(page + 1))

        return kwargs

    def make_page_link(self, page):
        return '{}?{}'.format(self.request.path, urlencode({'page': page}))


class V2SearchView(FormView):
    template_name = 'tmdb/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)


class V2ShowView(TemplateView):
    template_name = 'tmdb/show.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        kwargs.update(show=get_show(id))
        user = self.request.user
        if user.is_authenticated:
            progress = Progress.objects.filter(user=user, show_id=id).first()
            kwargs.update(progress=progress)
        return kwargs
