from typing import Any
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView

from ..models import BookInstance

class BorrowedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned')
    template_name = 'catalog/bookinstance_list_borrowed.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back'))
