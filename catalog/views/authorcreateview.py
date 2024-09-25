from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView

from ..models import Author

class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'
