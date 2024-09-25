from django.views.generic import DetailView

from ..models import Author

class AuthorDetailView(DetailView):
    model = Author
