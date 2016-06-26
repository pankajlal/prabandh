from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

SUBMITTER = (('parent', 'parent'),
             ('faculty','faculty'),
             ('expert', 'expert'),
             ('child', 'child')
             )
class Observation(models.Model):
    instance_id = models.CharField(max_length=100)
    submission_date = models.DateField()
    is_complete = models.BooleanField(default=True)
    date_marked_as_complete = models.DateField()
    image = models.ImageField()
    observation = models.TextField()
    child = models.ForeignKey(User)
    submitter = models.CharField(max_length=10, choices=SUBMITTER)
    start_time = models.DateField()