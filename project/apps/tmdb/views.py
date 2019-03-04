from urllib.parse import urlencode, urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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
from .utils import (
    get_air_dates,
    get_next_episode,
    get_popular_shows,
    get_show,
    get_shows,
    get_status_value,
    mark_saved_shows,
)


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

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        self.update_progresses()
        progresses = Progress.objects.filter(user=self.request.user)
        kwargs.update(
            available=[progress for progress in progresses if progress.list_in_available],
            scheduled=[progress for progress in progresses if progress.list_in_scheduled],
            unavailable=[progress for progress in progresses if progress.list_in_unavailable],
            paused=[progress for progress in progresses if progress.list_in_paused],
            finished=[progress for progress in progresses if progress.list_in_finished],
            stopped=[progress for progress in progresses if progress.list_in_stopped],
        )
        return kwargs

    def update_progresses(self):
        params_list = self.get_params_list_to_update()
        next_air_dates = self.get_next_air_dates(params_list)
        for params in params_list:
            for show_id, next_air_date in next_air_dates:
                if params['show_id'] == show_id:
                    params.update(next_air_date=next_air_date)
                    break
            Progress.objects.filter(user=self.request.user, show_id=params['show_id']).update(**params)

    def get_show_ids_to_update(self):
        return Progress.objects.filter(
            ~Q(
                next_season__isnull=False,
                next_episode__isnull=False,
                next_air_date__isnull=False,
            ),
            user=self.request.user,
            status=Progress.FOLLOWING,
        ).values_list('show_id', flat=True)

    def get_params_list_to_update(self):
        show_ids = self.get_show_ids_to_update()
        shows = get_shows(show_ids)
        params_list = []
        for show in shows:
            progress = Progress.objects.get(show_id=show['id'])
            next_season, next_episode = get_next_episode(
                show,
                progress.current_season,
                progress.current_episode,
            )
            params_list.append({
                'show_id': show['id'],
                'show_name': show['original_name'],
                'show_poster_path': show['poster_path'],
                'show_status': get_status_value(show['status']),
                'next_season': next_season,
                'next_episode': next_episode,
            })
        return params_list

    def get_next_air_dates(self, progresses):
        params_list = []
        for progress in progresses:
            if not (progress['next_season'] and progress['next_episode']):
                continue
            params_list.append({
                'show_id': progress['show_id'],
                'season': progress['next_season'],
                'episode': progress['next_episode'],
            })
        results = get_air_dates(params_list)
        return [(result['show_id'], result['air_date']) for result in results]


class ProgressMixin:
    template_name = 'tmdb/progress.html'
    form_class = ProgressForm

    @property
    def show(self):
        if not hasattr(self, '_show'):
            self._show = get_show(self.kwargs['show_id'])
        return self._show

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(show=self.show)
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            user=self.request.user,
            show=self.show,
        )
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            show_id=self.show['id'],
            show_name=self.show['original_name'],
            show_poster_path=self.show['poster_path'],
            show_status=get_status_value(self.show['status']),
        )
        return initial

    def get_success_url(self):
        default_success_url = reverse('tmdb:v2_popular_shows')
        return self.request.session.get('previous_path', default_success_url)


class V2ProgressCreateView(ProgressMixin, CreateView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:v2_signup'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class V2ProgressUpdateView(ProgressMixin, LoginRequiredMixin, UpdateView):
    def get_object(self, queryset=None):
        return get_object_or_404(Progress, user=self.request.user, show_id=self.kwargs['show_id'])

    def get_initial(self):
        initial = super().get_initial()
        last_watched = '{}-{}'.format(self.object.current_season, self.object.current_episode)
        initial.update(last_watched=last_watched)
        return initial


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
