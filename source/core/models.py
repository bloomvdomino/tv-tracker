import uuid

from django.db import models


class BaseModel(models.Model):
    """
    A base class from which all model classes should inherit.
    """

    id = models.BigAutoField(primary_key=True, editable=False, verbose_name="ID")
    created = models.DateTimeField(auto_now_add=True, verbose_name="created")
    updated = models.DateTimeField(auto_now=True, verbose_name="updated")

    class Meta:
        abstract = True


class BaseUUIDModel(BaseModel):
    """
    A base class which uses UUID for its primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")

    class Meta:
        abstract = True
