from django.contrib import admin

from .models import Parent
# Register your models here.

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):

    def full_name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
