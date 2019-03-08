from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .forms import ContactForm
from .serializers import ContactSerializer


class ContactView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactSerializer


class IndexView(View):
    def get(self, request, *args, **kwargs):
        url_name = 'v2_progresses' if request.user.is_authenticated else 'v2_popular_shows'
        return redirect(reverse('tmdb:{}'.format(url_name)))


class V2ContactView(CreateView):
    template_name = 'website/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('website:v2_contact')

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
