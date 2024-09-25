from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView

from ..models import Book

class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ('title', 'author', 'summary', 'isbn', 'genre', 'language')
    permission_required = 'catalog.add_book'
