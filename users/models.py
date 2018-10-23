from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.


class Faculty(models.Model):
    user = models.OneToOneField(User)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.user.get_full_name()

class Sakha(models.Model):
    user = models.OneToOneField(User)

    class Meta:
        verbose_name_plural="Sakhayein"

    def __str__(self):
        return self.user.get_full_name()

class Parent(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.get_full_name()

class Learner(models.Model):
    user = models.OneToOneField(User)
    parent = models.ForeignKey(Parent)
    sakha = models.ForeignKey(Sakha)

    def __str__(self):
        return self.user.get_full_name()
   
    class Meta:
        ordering = ['user__first_name','user__last_name',]
    
admin.site.register(Faculty)
admin.site.register(Sakha)
admin.site.register(Parent)
admin.site.register(Learner)
