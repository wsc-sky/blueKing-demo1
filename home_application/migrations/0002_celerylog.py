# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.CharField(max_length=40)),
                ('app_id', models.CharField(max_length=10)),
                ('task_id', models.CharField(max_length=10)),
                ('log', models.CharField(max_length=2000)),
            ],
        ),
    ]
