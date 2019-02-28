from urllib.parse import urlencode, urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    FormView,
    TemplateView,
    UpdateView,
    View,
)
from rest_framework import mixins, viewsets

from .forms import ProgressForm, SearchForm
from .models import Progress
from .serializers import ProgressSerializer
from .utils import get_popular_shows, get_show, mark_saved_shows


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


class V2ProgressCreateView(CreateView):
    template_name = 'tmdb/progress.html'
    form_class = ProgressForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:v2_signup'))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(show=get_show(self.kwargs['show_id']))
        return kwargs

    def get_initial(self):
        show = get_show(self.kwargs['show_id'])

        for status, label in Progress.SHOW_STATUS_CHOICES:
            if label == show['status']:
                show_status = status
                break

        initial = super().get_initial()
        initial.update(
            show_id=show['id'],
            show_name=show['original_name'],
            show_poster_path=show['poster_path'],
            show_status=show_status,
        )
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        default_success_url = reverse('tmdb:v2_popular_shows')
        return self.request.session.get('previous_path', default_success_url)


class V2ProgressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'tmdb/progress.html'
    form_class = ProgressForm

    def get_object(self, queryset=None):
        return get_object_or_404(Progress, user=self.request.user, show_id=self.kwargs['show_id'])

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(show=get_show(self.kwargs['show_id']))
        return kwargs


class V2PopularShowsView(TemplateView):
    template_name = 'tmdb/popular_shows.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        min_page = 1
        max_page = 1000

        page = int(self.request.GET.get('page', min_page))
        page = page if page >= min_page else min_page
        page = page if page <= max_page else max_page
        shows = get_popular_shows(page)
        shows = mark_saved_shows(shows, self.request.user)
        kwargs.update(current_page=page, shows=shows)

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
        form.results = mark_saved_shows(form.results, self.request.user)
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)


class V2ShowView(View):
    def get(self, request, *args, **kwargs):
        self.set_previous_path()

        user = request.user
        show_id = self.kwargs['id']
        if user.is_authenticated and Progress.objects.filter(user=user, show_id=show_id).exists():
            action = 'update'
        else:
            action = 'create'
        url = reverse('tmdb:v2_progress_{}'.format(action), kwargs={'show_id': show_id})
        return redirect(url)

    def set_previous_path(self):
        url = self.request.META.get('HTTP_REFERER')
        if url:
            components = urlparse(url)
            path = components.path
            if components.query:
                path = '{}?{}'.format(path, components.query)
            self.request.session['previous_path'] = path
        else:
            del self.request.session['previous_path']
