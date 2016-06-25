from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.


class Faculty(models.Model):
    user = models.OneToOneField(User)

class Sakha(models.Model):
    user = models.OneToOneField(User)

class Parent(models.Model):
    user = models.OneToOneField(User)

class Learner(models.Model):
    user = models.OneToOneField(User)
    parent = models.ForeignKey(Parent)
    sakha = models.ForeignKey(Sakha)


admin.site.register(Faculty)
admin.site.register(Sakha)
admin.site.register(Parent)
admin.site.register(Learner)