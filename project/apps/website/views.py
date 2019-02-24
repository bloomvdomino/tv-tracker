from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import ContactSerializer


class ContactView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ContactSerializer


class V2ContactView(TemplateView):
    template_name = 'website/contact.html'
