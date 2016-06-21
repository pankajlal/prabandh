from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from isbntools import app

# Create your models here.

class Isbn(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    year = models.DateField()
    publisher = models.CharField(max_length=100)

class State(models.Model):
    name = models.CharField(max_length=10)

class Book(models.Model):
    isbn = models.ForeignKey(Isbn)
    beme_id = models.IntegerField()
    current_state = models.ForeignKey(State)

ACTION_CHOICES = (
    ('Issue', 'Issue'),
    ('Return', 'Return'),
    ('Procured', 'Procured'),
    ('Destroyed', 'Destroyed'),
    ('Lost', 'Lost'),
    ('Found', 'Found')
)

class Transaction(models.Model):
    book = models.ForeignKey(Book)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    logged_in_user = models.ForeignKey(User, related_name='logged_in_user')
    transaction_user = models.ForeignKey(User, related_name='transaction_user')

admin.site.register(Isbn)