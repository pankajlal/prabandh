# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-25 01:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obspost', '0002_childsheet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observation',
            name='date_marked_as_complete',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='is_complete',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='observation',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='observation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
