from django.contrib import admin

from .models import Isbn
# Register your models here.

@admin.register(Isbn)
class IsbnAdmin(admin.ModelAdmin):
    fields=('code',)
    list_display = ('code', 'title', 'year', 'publisher')
