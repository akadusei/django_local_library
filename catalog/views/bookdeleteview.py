from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from ..models import Book

class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self, _):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as error:
            return HttpResponseRedirect(reverse(
                'book-delete',
                kwargs={'pk': self.object.pk}
            ))
