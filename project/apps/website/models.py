from django.db import models

from project.apps.accounts.models import User
from project.core.models import BaseModel


class Contact(BaseModel):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             verbose_name="user")
    message = models.TextField(verbose_name="message")

    class Meta:
        ordering = ['-created']
        verbose_name = "contact"
        verbose_name_plural = "contacts"
