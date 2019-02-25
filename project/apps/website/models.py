from django.conf import settings
from django.db import models

from project.core.models import BaseModel


class Contact(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, blank=True, null=True, verbose_name="user")
    email = models.EmailField(verbose_name="email")
    message = models.TextField(verbose_name="message")

    class Meta:
        ordering = ['-created']
        verbose_name = "contact"
        verbose_name_plural = "contacts"
