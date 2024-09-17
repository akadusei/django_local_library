from django.db.models import (
    CharField,
    ForeignKey,
    ManyToManyField,
    Model,
    RESTRICT,
    SET_NULL,
    TextField
)
from django.urls import reverse

from .author import Author
from .genre import Genre
from .language import Language

class Book(Model):
    LANGUAGES = {
        'en': 'English',
        'fs': 'Farsi',
    }

    title = CharField(max_length=200)
    author = ForeignKey(Author, on_delete=RESTRICT, null=True)
    language = ForeignKey(Language, on_delete=SET_NULL, null=True)

    summary = TextField(
        max_length=1000,
        help_text='Enter a brief description of the book'
    )

    isbn = CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='13 Character ' \
            '<a href="https://www.isbn-international.org/content/what-isbn' \
            '">ISBN number</a>'
    )

    genre = ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('book-detail', args=[str(self.id)])
