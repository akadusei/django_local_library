from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from ..models import Author

class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, _):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as error:
            return HttpResponseRedirect(reverse(
                'author-delete',
                kwargs={'pk': self.object.pk}
            ))
