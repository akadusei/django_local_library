# from typing import Any

from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

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

class BorrowedBooksListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    model = BookInstance
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned')
    template_name = 'catalog/bookinstance_list_borrowed.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back'))
