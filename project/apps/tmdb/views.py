from urllib.parse import urlencode, urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import resolve, reverse
from django.utils.functional import cached_property
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from .forms import ProgressForm, SearchForm
from .models import Progress
from .utils import (
    add_progress_info,
    get_air_dates,
    get_next_episode,
    get_popular_shows,
    get_show,
    get_shows,
    get_status_value,
)


class ProgressesView(LoginRequiredMixin, TemplateView):
    template_name = 'tmdb/progresses.html'

    @property
    def progresses(self):
        return Progress.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        self.update_progresses_info()
        self.update_progresses_status()

        context = super().get_context_data(**kwargs)
        context.update(
            saved_count=self.request.user.progress_set.count(),
            following_count=self.request.user.progress_set.filter(status=Progress.FOLLOWING).count(),
            available=[progress for progress in self.progresses if progress.list_in_available],
            scheduled=[progress for progress in self.progresses if progress.list_in_scheduled],
            unavailable=[progress for progress in self.progresses if progress.list_in_unavailable],
            paused=[progress for progress in self.progresses if progress.list_in_paused],
            finished=[progress for progress in self.progresses if progress.list_in_finished],
            stopped=[progress for progress in self.progresses if progress.list_in_stopped],
        )
        return context

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


class PopularShowsView(TemplateView):
    template_name = 'tmdb/popular_shows.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        min_page = 1
        max_page = 1000

        page = int(self.request.GET.get('page', min_page))
        page = page if page >= min_page else min_page
        page = page if page <= max_page else max_page
        shows = get_popular_shows(page)
        shows = add_progress_info(shows, self.request.user)
        context.update(current_page=page, shows=shows)

        if page - 1 >= min_page:
            context.update(previous_page_link=self.make_page_link(page - 1))

        if page + 1 <= max_page:
            context.update(next_page_link=self.make_page_link(page + 1))

        return context

    def make_page_link(self, page):
        return '{}?{}'.format(self.request.path, urlencode({'page': page}))


class SearchView(FormView):
    template_name = 'tmdb/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        form.results = add_progress_info(form.results, self.request.user)
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)


class ProgressEditMixin:
    template_name = 'tmdb/progress.html'
    form_class = ProgressForm

    @property
    def show_id(self):
        return self.kwargs['show_id']

    @cached_property
    def show(self):
        return get_show(self.show_id)

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_to_create_or_update()
        if redirect:
            return redirect

        self.set_progress_edit_success_url()
        return super().get(request, *args, **kwargs)

    def redirect_to_create_or_update(self):
        action = None
        current_url = resolve(self.request.path_info).url_name
        progress = self.get_object()
        if current_url == 'progress_create' and progress:
            action = 'update'
        elif current_url == 'progress_update' and not progress:
            action = 'create'
        if action:
            to = 'tmdb:progress_{}'.format(action)
            return redirect(reverse(to, kwargs={'show_id': self.show_id}))

    def set_progress_edit_success_url(self):
        http_referer = self.request.META.get('HTTP_REFERER')
        if http_referer:
            components = urlparse(http_referer)
            url = components.path
            if resolve(url).url_name in ['progresses', 'popular_shows', 'search']:
                if components.query:
                    url = '{}?{}'.format(url, components.query)
                self.request.session['progress_edit_success_url'] = url
                return
        url = reverse('tmdb:popular_shows')
        self.request.session['progress_edit_success_url'] = url

    def get_object(self, queryset=None):
        user = self.request.user
        if not user.is_authenticated:
            return None
        return user.progress_set.filter(show_id=self.show_id).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(show=self.show)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user, show=self.show)
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            show_id=self.show_id,
            show_name=self.show['original_name'],
            show_poster_path=self.show['poster_path'],
            show_status=get_status_value(self.show['status']),
        )
        return initial

    def get_success_url(self):
        return self.request.session['progress_edit_success_url']


class ProgressCreateView(ProgressEditMixin, CreateView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            to = reverse('accounts:login')
            return redirect('{}?{}'.format(to, urlencode({'next': request.path})))
        return super().post(request, *args, **kwargs)


class ProgressUpdateView(ProgressEditMixin, LoginRequiredMixin, UpdateView):
    def get_initial(self):
        initial = super().get_initial()
        last_watched = '{}-{}'.format(self.object.current_season, self.object.current_episode)
        initial.update(status=self.object.status, last_watched=last_watched)
        return initial
