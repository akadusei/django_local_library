from django.db.models import CharField, Model, UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse

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
