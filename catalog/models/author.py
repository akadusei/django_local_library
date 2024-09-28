from django.db.models import CharField, DateField, Model
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

    @property
    def age_range(self) -> str:
        if self.date_of_birth and self.date_of_death:
            return f'{self.date_of_birth} - {self.date_of_death}'
        elif self.date_of_birth:
            return f'{self.date_of_birth} - '
        elif self.date_of_death:
            return f' - {self.date_of_death}'
        else:
            return ''

    class Meta:
        ordering = ['last_name', 'first_name']
