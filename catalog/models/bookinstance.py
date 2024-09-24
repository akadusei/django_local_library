from datetime import date
import uuid

from django.conf import settings
from django.db.models import (
    CharField,
    DateField,
    ForeignKey,
    Model,
    RESTRICT,
    SET_NULL,
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

    borrower = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self) -> bool:
        return self.due_back and date.today() > self.due_back

    def display_book_title(self) -> str:
        return self.book.title

    display_book_title.short_description = 'Title'

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'), )
