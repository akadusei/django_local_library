from django.db.models import CharField, Model, UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse

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
