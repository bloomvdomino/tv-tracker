from urllib.parse import urlencode, urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse
from django.utils.functional import cached_property
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
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

    @cached_property
    def progresses(self):
        return Progress.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        self.update_progresses_info()
        self.update_progresses_status()

        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            saved_count=self.request.user.added_progresses_count,
            following_count=len([progress for progress in self.progresses if progress.status == Progress.FOLLOWING]),
            max_following_count=self.request.user.max_followed_progresses,
            available=[progress for progress in self.progresses if progress.list_in_available],
            scheduled=[progress for progress in self.progresses if progress.list_in_scheduled],
            unavailable=[progress for progress in self.progresses if progress.list_in_unavailable],
            paused=[progress for progress in self.progresses if progress.list_in_paused],
            finished=[progress for progress in self.progresses if progress.list_in_finished],
            stopped=[progress for progress in self.progresses if progress.list_in_stopped],
        )
        return kwargs

    def update_progresses_info(self):
        params_list = self.get_params_list_to_update()
        next_air_dates = self.get_next_air_dates(params_list)
        for params in params_list:
            for show_id, next_air_date in next_air_dates:
                if params['show_id'] == show_id:
                    params.update(next_air_date=next_air_date)
                    break
            self.progresses.filter(show_id=params['show_id']).update(**params)

    def get_show_ids_to_update(self):
        return self.progresses.filter(
            ~Q(
                next_season__isnull=False,
                next_episode__isnull=False,
                next_air_date__isnull=False,
            ),
            status=Progress.FOLLOWING,
        ).values_list('show_id', flat=True)

    def get_params_list_to_update(self):
        show_ids = self.get_show_ids_to_update()
        shows = get_shows(show_ids)
        params_list = []
        for show in shows:
            progress = Progress.objects.get(user=self.request.user, show_id=show['id'])
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

    def update_progresses_status(self):
        """
        Update progress status to stopped if the show is finished and the user
        also watched all episodes.
        """
        self.progresses.filter(
            ~Q(status=Progress.STOPPED),
            show_status__in=[Progress.ENDED, Progress.CANCELED],
            next_air_date__isnull=True,
        ).update(status=Progress.STOPPED)


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


class ShowMixin:
    show_id_url_kwarg = 'id'

    @property
    def show_id(self):
        return self.kwargs[self.show_id_url_kwarg]

    @cached_property
    def show(self):
        return get_show(self.show_id)


class ProgressFormMixin:
    form_class = ProgressForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            user=self.request.user,
            show=self.show,
        )
        return kwargs


class V2ShowView(ShowMixin, ProgressFormMixin, FormView):
    template_name = 'tmdb/progress.html'

    @cached_property
    def progress(self):
        user = self.request.user
        if not user.is_authenticated:
            return None
        return Progress.objects.filter(user=user, show_id=self.show_id).first()

    def get(self, request, *args, **kwargs):
        self.set_progress_edit_success_url()
        return super().get(request, *args, **kwargs)

    def set_progress_edit_success_url(self):
        http_referer = self.request.META.get('HTTP_REFERER')
        if http_referer:
            components = urlparse(http_referer)
            url = components.path
            if resolve(url).namespace == 'tmdb':
                if components.query:
                    url = '{}?{}'.format(url, components.query)
                self.request.session['progress_edit_success_url'] = url
                return
        url = reverse('tmdb:v2_popular_shows')
        self.request.session['progress_edit_success_url'] = url

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(
            show=self.show,
            progress=self.progress,
            post_url=self.get_post_url(),
        )
        return kwargs

    def get_post_url(self):
        action = 'update' if self.progress else 'create'
        name = 'tmdb:v2_progress_{}'.format(action)
        kwargs = {'show_id': self.show_id}
        return reverse(name, kwargs=kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            show_id=self.show_id,
            show_name=self.show['original_name'],
            show_poster_path=self.show['poster_path'],
            show_status=get_status_value(self.show['status']),
        )
        if self.progress:
            last_watched = '{}-{}'.format(self.progress.current_season, self.progress.current_episode)
            initial.update(
                status=self.progress.status,
                last_watched=last_watched,
            )
        return initial


class ProgressEditMixin:
    def get(self, request, *args, **kwargs):
        return redirect(reverse('tmdb:v2_show', kwargs={'id': self.show_id}))

    def get_success_url(self):
        return self.request.session['progress_edit_success_url']


class V2ProgressCreateView(
    ShowMixin,
    ProgressFormMixin,
    ProgressEditMixin,
    LoginRequiredMixin,
    CreateView,
):
    show_id_url_kwarg = 'show_id'


class V2ProgressUpdateView(
    ShowMixin,
    ProgressFormMixin,
    ProgressEditMixin,
    LoginRequiredMixin,
    UpdateView,
):
    show_id_url_kwarg = 'show_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Progress, user=self.request.user, show_id=self.show_id)
