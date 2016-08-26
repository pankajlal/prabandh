from django.contrib import admin

# Register your models here.


# Register your models here.
from .models import ChildSheet

@admin.register(ChildSheet)
class ChildSheetAdmin(admin.ModelAdmin):
    list_display = ('learner', 'sheetcode', 'foldercode')