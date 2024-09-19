# from typing import Any

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

    context = {
        'num_authors': num_authors,
        'num_books': num_books,
        'num_genres': num_genres,
        'num_harry_potter_books': num_harry_potter,
        'num_instances': num_instances,
        'num_instances_available': num_available
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
