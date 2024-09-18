from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

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
