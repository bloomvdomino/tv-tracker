# Generated by Django 2.1.7 on 2019-03-16 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_accounts', '0005_auto_20190309_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time_zone',
            field=models.CharField(choices=[('UTC', 'UTC'), ('America/New_York', 'New York'), ('America/Sao_Paulo', 'São Paulo'), ('Asia/Shanghai', 'Shanghai')], default='UTC', max_length=32, verbose_name='time zone'),
        ),
    ]