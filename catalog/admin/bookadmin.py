from django.contrib import admin
from ..models import Book, BookInstance

class BookInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

# admin.site.register(Book, BookAdmin)
