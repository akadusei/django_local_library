from django.contrib import admin
from ..models import Author, Book

class BookInline(admin.StackedInline):
    extra = 0
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

# admin.site.register(Author, AuthorAdmin)
