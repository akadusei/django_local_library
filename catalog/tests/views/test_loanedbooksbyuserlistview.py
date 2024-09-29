import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import Author, Book, BookInstance, Genre, Language

User = get_user_model()

class LoanedBooksByUserListViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            username='testuser1',
            password='1X<ISRUkw+tuK'
        )

        user2 = User.objects.create_user(
            username='testuser2',
            password='2HJ1vRV0Z&3iD'
        )

        user1.save()
        user2.save()

        Genre.objects.create(name='Fantasy')

        author = Author.objects.create(first_name='John', last_name='Smith')
        language = Language.objects.create(name='English')

        book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=author,
            language=language,
        )

        # Create genre as a post-step
        # Direct assignment of many-to-many types not allowed.
        genres = Genre.objects.all()
        book.genre.set(genres)

        book.save()

        number_of_copies = 30

        for book_copy in range(number_of_copies):
            return_date = (timezone.localtime() +
                datetime.timedelta(days=book_copy%5))

            the_borrower = user1 if book_copy % 2 else user2
            status = 'm'

            BookInstance.objects.create(
                book=book,
                imprint='Unlikely Imprint, 2016',
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))

        self.assertRedirects(
            response,
            '/accounts/login/?next=/catalog/mybooks/'
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')

        self.assertTemplateUsed(
            response,
            'catalog/bookinstance_list_borrowed_user.html'
        )

    def test_only_borrowed_books_in_list(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')

        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)

        for book in BookInstance.objects.all()[:10]:
            book.status = 'o'
            book.save()

        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTrue('bookinstance_list' in response.context)

        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(bookitem.status, 'o')
            self.assertEqual(bookitem.borrower, response.context['user'])

    def test_pages_ordered_by_due_date(self):
        for book in BookInstance.objects.all():
            book.status='o'
            book.save()

        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0

        for book in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back

    def test_pagination_is_ten(self):
        for book in BookInstance.objects.all():
            book.status='o'
            book.save()

        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(f'{reverse('my-borrowed')}?page=2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')

        self.assertTrue(response.context['is_paginated'] == True)

        # '5' because only half of the 30 books belong to this user
        self.assertEqual(len(response.context['bookinstance_list']), 5)
