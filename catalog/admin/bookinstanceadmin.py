from django.contrib import admin
from ..models import BookInstance

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back', 'borrower')})
    )

    list_display = ('id', 'display_book_title', 'status', 'borrower', 'due_back')
    list_filter = ('status', 'due_back')

# admin.site.register(BookInstance, BookInstanceAdmin)
