from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from isbntools import app

# Create your models here.

class Isbn(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=400)
    author = models.CharField(max_length=200)
    year = models.DateField()
    publisher = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author', related_name='authors')

    def __str__(self):
        return self.title

class State(models.Model):
    name = models.CharField(max_length=10)

class BookItem(models.Model):
    isbn = models.ForeignKey(Isbn)
    beme_id = models.IntegerField()
    current_state = models.ForeignKey(State)
    owner = models.ForeignKey(User, default=None, blank=True)

    #def __str__(self):
    #    return self.isbn.name + " " + self.current_state.name

class Author(models.Model):
    name = models.CharField(max_length=100, blank=None, unique=True)

ACTION_CHOICES = (
    ('Issue', 'Issue'),
    ('Return', 'Return'),
    ('Procured', 'Procured'),
    ('Destroyed', 'Destroyed'),
    ('Lost', 'Lost'),
    ('Found', 'Found')
)

class Transaction(models.Model):
    book = models.ForeignKey(BookItem)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    logged_in_user = models.ForeignKey(User, related_name='logged_in_user')
    transaction_user = models.ForeignKey(User, related_name='transaction_user')

