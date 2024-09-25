from django.views.generic import ListView

from ..models import Book

class BookListView(ListView):
    model = Book
    paginate_by = 10

    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context['some_data'] = 'This is just some data'
    #     return context

    # def get_queryset(self):
    #     return Book.objects.all()
