from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.contrib import admin
# Create your models here.
from django.contrib import admin

SUBMITTER = (('parent', 'parent'),
             ('faculty','faculty'),
             ('expert', 'expert'),
             ('child', 'child')
             )

from users.models import Learner

class Observation(models.Model):
    instance_id = models.CharField(max_length=100)
    submission_date = models.DateField()
    image = models.ImageField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    child = models.ForeignKey(User, null=True)
    submitter = models.CharField(max_length=10, choices=SUBMITTER, blank=True, null=True)

    def __str__(self):
        return self.observation

class ObservedChild(models.Model):
    observation = models.ForeignKey(Observation)
    learner = models.ForeignKey(Learner)

class ChildSheet(models.Model):
    sheetcode = models.CharField(max_length=200)
    foldercode = models.CharField(max_length=200)
    learner = models.OneToOneField(Learner)

    def __str__(self):
        return self.learner.user.get_full_name() + " - Sheet: %s" % (self.sheetcode)
