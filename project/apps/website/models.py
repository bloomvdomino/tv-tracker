from django.db import models

from project.core.models import BaseModel


class Contact(BaseModel):
    email = models.EmailField(verbose_name="email")
    message = models.TextField(verbose_name="message")

    class Meta:
        ordering = ['-created']
        verbose_name = "contact"
        verbose_name_plural = "contacts"
