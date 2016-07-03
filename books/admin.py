from django.contrib import admin

from .models import Isbn
# Register your models here.

@admin.register(Isbn)
class IsbnAdmin(admin.ModelAdmin):

    def authors_str(self, obj):
        a_str = ''
        for a in obj.authors.all():
            a_str = a_str + a.name + ", "
        a_str = a_str.rstrip(", ")
        return a_str
    fields=('code',)
    list_display = ('code', 'title', 'year', 'publisher', 'authors_str')
