from typing import Any
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.db.models.query import QuerySet
from django.views.generic import ListView

from ..models import BookInstance

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects
            .filter(borrower=self.request.user, status__exact='o')
            .order_by('due_back'))
