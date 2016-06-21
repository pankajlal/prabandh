# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 14:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beme_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Isbn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=200)),
                ('year', models.DateField()),
                ('publisher', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Issue', 'Issue'), ('Return', 'Return'), ('Procured', 'Procured'), ('Destroyed', 'Destroyed'), ('Lost', 'Lost'), ('Found', 'Found')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
                ('logged_in_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL)),
                ('transaction_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='current_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.State'),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Isbn'),
        ),
    ]
