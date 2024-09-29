import datetime

from django.test import TestCase

from catalog.models import Author

class AuthorTest(TestCase):
    def test_first_name_label(self):
        author = Author(first_name='Big', last_name='Bob')
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author(first_name='Big', last_name='Bob')
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author(first_name='Big', last_name='Bob')
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author(first_name='Big', last_name='Bob')
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author(first_name='Big', last_name='Bob')
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author(first_name='Big', last_name='Bob')
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author(first_name='Big', last_name='Bob')
        full_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), full_name)

    def test_get_absolute_url(self):
        author = Author.objects.create(first_name='Big', last_name='Bob')
        expected_url = f'/catalog/author/{author.id}/'
        self.assertEqual(author.get_absolute_url(), expected_url)

    def test_age_range(self):
        author = Author(first_name='Big', last_name='Bob')
        self.assertEqual(author.age_range, '')

    def test_age_range_given_birth(self):
        author = Author(
            first_name='Big',
            last_name='Bob',
            date_of_birth=datetime.date(1990, 5, 24),
        )

        expected_range = f'{author.date_of_birth} - '
        self.assertEqual(author.age_range, expected_range)

    def test_age_range_given_death(self):
        author = Author(
            first_name='Big',
            last_name='Bob',
            date_of_death=datetime.date(2023, 4, 13),
        )

        expected_range = f' - {author.date_of_death}'
        self.assertEqual(author.age_range, expected_range)

    def test_age_range_given_birth_death(self):
        author = Author(
            first_name='Big',
            last_name='Bob',
            date_of_birth=datetime.date(1990, 5, 24),
            date_of_death=datetime.date(2023, 4, 13),
        )

        expected_range = f'{author.date_of_birth} - {author.date_of_death}'
        self.assertEqual(author.age_range, expected_range)
