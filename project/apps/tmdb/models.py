from django.conf import settings
from django.db import models

from project.core.models import BaseModel


class Progress(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="user")

    show_id = models.PositiveIntegerField(verbose_name="show ID")
    show_name = models.CharField(max_length=64, verbose_name="show name")
    show_poster_path = models.CharField(max_length=64, blank=True, default='',
                                        verbose_name="show poster path")

    current_season = models.PositiveSmallIntegerField(default=0, verbose_name="current season")
    current_episode = models.PositiveSmallIntegerField(default=0, verbose_name="current episode")
    next_season = models.PositiveSmallIntegerField(blank=True, null=True, default=1,
                                                   verbose_name="next season")
    next_episode = models.PositiveSmallIntegerField(blank=True, null=True, default=1,
                                                    verbose_name="next episode")
    next_air_date = models.DateField(blank=True, null=True, verbose_name="next air date")

    class Meta:
        unique_together = (('user', 'show_id'),)
        ordering = ['-created']
        verbose_name = "progress"
        verbose_name_plural = "progresses"
