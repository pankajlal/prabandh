from django.contrib import admin

# Register your models here.


# Register your models here.
from .models import ChildSheet
from .models import Observation

@admin.register(ChildSheet)
class ChildSheetAdmin(admin.ModelAdmin):
    list_display = ('learner', 'sheetcode', 'foldercode')

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('submission_date', 'submitter', 'child', 'observation',)
    list_filter = ('submission_date','child__learner',)
    search_fields = ('child__first_name','observation',)
