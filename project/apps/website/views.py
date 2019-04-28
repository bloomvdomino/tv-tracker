from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View

from .forms import ContactForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        url_name = "progresses" if request.user.is_authenticated else "popular_shows"
        return redirect(reverse("tmdb:{}".format(url_name)))


class ContactView(CreateView):
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("website:contact")

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            initial.update(email=user.email)
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Your message has been sent, thank you for contacting us.")
        user = self.request.user
        if user.is_authenticated:
            form.instance.user = user
        return super().form_valid(form)
