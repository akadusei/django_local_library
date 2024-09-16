import uuid

from django.db.models import (
    CharField,
    DateField,
    ForeignKey,
    ManyToManyField,
    Model,
    RESTRICT,
    SET_NULL,
    TextField,
    UniqueConstraint,
    UUIDField
)
from django.db.models.functions import Lower
from django.urls import reverse

class Author(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField('Died', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self) -> str:
        return reverse('author-detail', args=[str(self.id)])

    class Meta:
        ordering = ['first_name', 'last_name']

class Genre(Model):
    name = CharField(
        max_length=200,
        unique=True,
        help_text='Enter a book genre ' \
            '(e.g. Science Fiction, French Poetry etc.)'
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message='Genre already exists ' \
                    '(case-insensitive match)'
            )
        ]

class Language(Model):
    name = CharField(
        max_length=200,
        unique=True,
        help_text="Enter the book's natural language " \
            "(eg: English, French, Japanese etc.)"
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('language-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message='Language already exists ' \
                    '(case-insensitive match)'
            )
        ]

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

class BookInstance(Model):
    LOAN_STATUS = {
        'm': 'Maintenance',
        'o': 'On loan',
        'a': 'Available',
        'r': 'Reserved'
    }

    id = UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this book across the whole library'
    )

    book = ForeignKey(Book, on_delete=RESTRICT, null=True)
    imprint = CharField(max_length=200)
    due_back = DateField(null=True, blank=True)

    status = CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    def __str__(self) -> str:
        return f'{self.id} ({self.book.title})'

    class Meta:
        ordering = ['due_back']
