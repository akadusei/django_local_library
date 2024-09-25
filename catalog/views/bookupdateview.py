from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView

from ..models import Book

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ('title', 'author', 'summary', 'isbn', 'genre', 'language')
    permission_required = 'catalog.change_book'
