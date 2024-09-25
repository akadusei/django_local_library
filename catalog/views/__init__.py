# from typing import Any
import datetime
from uuid import UUID

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from ..forms import RenewBookForm
from ..models import Author, Book, BookInstance, Genre

from .authorcreateview import AuthorCreateView
from .authordeleteview import AuthorDeleteView
from .authordetailview import AuthorDetailView
from .authorlistview import AuthorListView
from .authorupdateview import AuthorUpdateView
from .bookcreateview import BookCreateView
from .bookdeleteview import BookDeleteView
from .bookdetailview import BookDetailView
from .booklistview import BookListView
from .bookupdateview import BookUpdateView
from .borrowedbookslistview import BorrowedBooksListView
from .loanedbooksbyuserlistview import LoanedBooksByUserListView

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
