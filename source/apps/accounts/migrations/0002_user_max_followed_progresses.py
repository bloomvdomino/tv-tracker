# Generated by Django 2.0.7 on 2018-07-24 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("apps_accounts", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="max_followed_progresses",
            field=models.PositiveSmallIntegerField(
                default=8, verbose_name="max followed progresses"
            ),
        )
    ]
