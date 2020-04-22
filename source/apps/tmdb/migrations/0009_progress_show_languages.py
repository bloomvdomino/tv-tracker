# Generated by Django 3.0.3 on 2020-04-22 23:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps_tmdb", "0008_remove_progress_last_check"),
    ]

    operations = [
        migrations.AddField(
            model_name="progress",
            name="show_languages",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=8),
                default=list,
                size=None,
                verbose_name="show languages",
            ),
        ),
    ]
