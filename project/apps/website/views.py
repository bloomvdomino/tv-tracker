from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .forms import ContactForm
from .serializers import ContactSerializer


class ContactView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactSerializer


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
