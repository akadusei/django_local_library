# from typing import Any
import datetime
from uuid import UUID

from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import RenewBookForm
from .models import Author, Book, BookInstance, Genre

def index(request: HttpRequest) -> HttpResponse:
    num_authors = Author.objects.all().count()
    num_books = Book.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_available = BookInstance.objects.filter(status__exact='a').count()

    num_harry_potter = (Book.objects
        .filter(title__icontains='harry potter')
        .count())

    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_authors': num_authors,
        'num_books': num_books,
        'num_genres': num_genres,
        'num_harry_potter_books': num_harry_potter,
        'num_instances': num_instances,
        'num_instances_available': num_available,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request: HttpRequest, pk: UUID):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = (
            datetime.date.today() + datetime.timedelta(weeks=3)
        )

        form = RenewBookForm(initial={
            'renewal_date': proposed_renewal_date
        })

    context = {
        'book_instance': book_instance,
        'form': form,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorListView(ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(DetailView):
    model = Author

class BookListView(ListView):
    model = Book
    paginate_by = 10

    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context['some_data'] = 'This is just some data'
    #     return context

    # def get_queryset(self):
    #     return Book.objects.all()

class BookDetailView(DetailView):
    model = Book

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects
            .filter(borrower=self.request.user, status__exact='o')
            .order_by('due_back'))

class BorrowedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned')
    template_name = 'catalog/bookinstance_list_borrowed.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back'))

class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    permission_required = 'catalog.change_author'

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

class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ('title', 'author', 'summary', 'isbn', 'genre', 'language')
    permission_required = 'catalog.add_book'

class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ('title', 'author', 'summary', 'isbn', 'genre', 'language')
    permission_required = 'catalog.change_book'

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
