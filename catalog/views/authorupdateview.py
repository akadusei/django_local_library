from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView

from ..models import Author

class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    permission_required = 'catalog.change_author'
