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

    class Meta:
        ordering = ['first_name', 'last_name']
