from urllib.parse import urlencode, urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve, reverse
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, UpdateView

from source.apps.tmdb.forms import FilterForm, ProgressForm, SearchForm
from source.apps.tmdb.utils import get_popular_shows, get_show


class WatchNextView(LoginRequiredMixin, View):
    def patch(self, request, *args, **kwargs):
        progress = request.user.progress_set.get(show_id=kwargs["show_id"])
        progress.update_show_data()
        progress.watch_next()
        progress.stop_if_finished()
        progress.save()
        return HttpResponse()


class ProgressesView(LoginRequiredMixin, FormView):
    template_name = "tmdb/progresses.html"
    form_class = FilterForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context["form"]
        if self.request.method == "GET":
            context.update(**self.request.user.progresses_summary())
        elif form.is_valid():
            language = form.cleaned_data["language"]
            context.update(**self.request.user.progresses_summary(language=language))
        return context


class PopularShowsView(TemplateView):
    template_name = "tmdb/popular_shows.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        min_page = 1
        max_page = 1000

        page = int(self.request.GET.get("page", min_page))
        page = page if page >= min_page else min_page
        page = page if page <= max_page else max_page
        shows = get_popular_shows(page, user=self.request.user)
        context.update(current_page=page, shows=shows)

        if page - 1 >= min_page:
            context.update(previous_page_link=self._make_page_link(page - 1))

        if page + 1 <= max_page:
            context.update(next_page_link=self._make_page_link(page + 1))

        return context

    def _make_page_link(self, page):
        qs = urlencode({"page": page})
        return f"{self.request.path}?{qs}"


class SearchView(FormView):
    template_name = "tmdb/search.html"
    form_class = SearchForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)


class ProgressEditMixin:
    template_name = "tmdb/progress.html"
    form_class = ProgressForm

    @cached_property
    def show(self):
        return get_show(self.kwargs["show_id"], user=self.request.user)

    def get(self, request, *args, **kwargs):
        redirect = self._redirect_to_create_or_update()
        if redirect:
            return redirect

        self._set_progress_edit_success_url()
        return super().get(request, *args, **kwargs)

    def _redirect_to_create_or_update(self):
        action = None
        current_url = resolve(self.request.path_info).url_name
        progress = self.get_object()
        if current_url == "progress_create" and progress:
            action = "update"
        elif current_url == "progress_update" and not progress:
            action = "create"
        if action:
            to = f"tmdb:progress_{action}"
            return redirect(reverse(to, kwargs={"show_id": self.show.id}))

    def _set_progress_edit_success_url(self):
        http_referer = self.request.META.get("HTTP_REFERER")
        if http_referer:
            components = urlparse(http_referer)
            url = components.path
            if resolve(url).url_name in ["progresses", "popular_shows", "search"]:
                if components.query:
                    url = f"{url}?{components.query}"
                self.request.session["progress_edit_success_url"] = url
                return
        url = reverse("tmdb:popular_shows")
        self.request.session["progress_edit_success_url"] = url

    def get_object(self, queryset=None):
        user = self.request.user
        if not user.is_authenticated:
            return None
        return user.progress_set.filter(show_id=self.show.id).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(show=self.show)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(show=self.show)
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        last_aired_season, last_aired_episode = self.show.last_aired_episode
        initial.update(
            show_id=self.show.id,
            show_name=self.show.name,
            show_poster_path=self.show.poster_path,
            show_status=self.show.status_value,
            show_genres=self.show.genres,
            show_languages=self.show.languages,
            last_aired_season=last_aired_season,
            last_aired_episode=last_aired_episode,
        )
        return initial

    def form_valid(self, form):
        form.instance.update_next_air_date()
        form.instance.stop_if_finished()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.session["progress_edit_success_url"]


class ProgressCreateView(ProgressEditMixin, CreateView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            to = reverse("accounts:login")
            qs = urlencode({"next": request.path})
            return redirect(f"{to}?{qs}")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProgressUpdateView(ProgressEditMixin, LoginRequiredMixin, UpdateView):
    def get_initial(self):
        initial = super().get_initial()
        last_watched = f"{self.object.current_season}-{self.object.current_episode}"
        initial.update(status=self.object.status, last_watched=last_watched)
        return initial


class ProgressDeleteView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        request.user.progress_set.filter(show_id=kwargs["show_id"]).delete()
        return JsonResponse({"redirect_to": reverse("tmdb:progresses")})
