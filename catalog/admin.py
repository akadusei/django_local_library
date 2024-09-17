from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language

class BookInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance

class BookInline(admin.StackedInline):
    extra = 0
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back')})
    )

    list_display = ('id', 'display_book_title', 'status', 'due_back')
    list_filter = ('status', 'due_back')

# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance, BookInstanceAdmin)
# admin.site.register(Genre)
# admin.site.register(Language)
