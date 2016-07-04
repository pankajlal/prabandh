from django.contrib import admin

from .models import Isbn
# Register your models here.
from .models import BookItem
from .models import Transaction
@admin.register(Isbn)
class IsbnAdmin(admin.ModelAdmin):

    def authors_str(self, obj):
        a_str = ''
        for a in obj.authors.all():
            a_str = a_str + a.name + ", "
        a_str = a_str.rstrip(", ")
        return a_str
    list_display = ('code', 'title', 'year', 'publisher', 'authors_str')

@admin.register(BookItem)
class BookAdmin(admin.ModelAdmin):
    def held_by(self, obj):
        trs = Transaction.objects.filter(book = obj).order_by('created')
        if trs.count() > 0:
            tr = trs[0]
            return tr.transaction_user.get_full_name()
        else:
            return obj.owner.get_full_name()

    def book_title(self,obj):
        assert isinstance(obj, Book)
        return obj.isbn.title

    def current_state(self,obj):
        assert isinstance(obj, Book)
        return obj.current_state.name

    list_display = ('book_title', 'current_state', 'held_by')
    pass