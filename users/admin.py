from django.contrib import admin

from .models import Learner
from .models import Parent
# Register your models here.

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('full_name','children')

    def children(self, obj):
        children = obj.learner_set.all()
        names = [child.user.first_name + " " + child.user.last_name for child in children]
        return ', '.join(names)

    def full_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
