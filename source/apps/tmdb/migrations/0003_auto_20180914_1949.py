# Generated by Django 2.1.1 on 2018-09-14 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("apps_tmdb", "0002_auto_20180723_2232")]

    operations = [
        migrations.AlterModelOptions(
            name="progress",
            options={
                "ordering": ["-is_followed", "next_air_date", "show_name", "show_id"],
                "verbose_name": "progress",
                "verbose_name_plural": "progresses",
            },
        ),
        migrations.RenameField(model_name="progress", old_name="followed", new_name="is_followed"),
    ]
