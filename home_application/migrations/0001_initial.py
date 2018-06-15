# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='celery_task_control',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_stop', models.BooleanField(default=False)),
                ('run_type', models.CharField(max_length=10)),
                ('time', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operation_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator', models.CharField(max_length=100, null=True)),
                ('operationtype', models.TextField(max_length=100)),
                ('ostype', models.TextField(max_length=100)),
                ('tasktype', models.TextField(max_length=100)),
                ('operated_detail', models.TextField(max_length=1000)),
                ('when_created', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('os_type', models.CharField(max_length=10)),
                ('operation_type', models.CharField(max_length=10)),
                ('task_type', models.CharField(max_length=10)),
                ('servers', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('modified_by', models.CharField(max_length=100)),
                ('run_type', models.CharField(default=b'NOW', max_length=10)),
                ('time_set', models.CharField(max_length=50)),
                ('timer_hour', models.CharField(max_length=50, null=True)),
                ('timer_minu', models.CharField(max_length=50, null=True)),
                ('when_created', models.CharField(max_length=100)),
                ('when_modified', models.CharField(max_length=100)),
                ('celery_task_control', models.OneToOneField(to='home_application.celery_task_control')),
            ],
        ),
    ]
