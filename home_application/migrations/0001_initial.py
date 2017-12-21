# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('job_id', models.AutoField(serialize=False, primary_key=True)),
                ('task_id', models.CharField(max_length=10)),
                ('task_name', models.CharField(max_length=50)),
                ('app_id', models.CharField(max_length=10)),
                ('app_name', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=20)),
                ('user', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('totalTime', models.CharField(max_length=10)),
                ('step', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'history_tab',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_id', models.IntegerField()),
                ('content', models.CharField(max_length=2000)),
            ],
            options={
                'db_table': 'task_log_tab',
            },
        ),
    ]
