from django.contrib import admin
from .models import BorrowedBook

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'return_date', 'status', 'is_overdue')
    list_filter = ('borrow_date', 'due_date', 'return_date', 'status')
    search_fields = ('user__username', 'book__title', 'book__isbn')
    raw_id_fields = ('user', 'book') # Good for large number of users/books

    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'

