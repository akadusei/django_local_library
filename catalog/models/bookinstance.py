import uuid

from django.db.models import (
    CharField,
    DateField,
    ForeignKey,
    Model,
    RESTRICT,
    UUIDField
)

from .book import Book

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

    def display_book_title(self) -> str:
        return self.book.title

    display_book_title.short_description = 'Title'

    class Meta:
        ordering = ['due_back']
