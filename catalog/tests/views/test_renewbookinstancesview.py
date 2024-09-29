import datetime
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
# from django.utils import timezone

from catalog.models import Author, Book, BookInstance, Genre, Language

User = get_user_model()

class RenewBookInstancesViewTest(TestCase):
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

        permission = Permission.objects.get(name='Set book as returned')
        user2.user_permissions.add(permission)
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
        genre_objects_for_book = Genre.objects.all()
        book.genre.set(genre_objects_for_book)
        book.save()

        # Create a BookInstance object for user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=user1,
            status='o',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=user2,
            status='o',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk}
        ))

        # Manually check redirect
        # (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk}
        ))

        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance2.pk}
        ))

        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk}
        ))

        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        uid = uuid.uuid4()
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': uid}
        ))

        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk}
        ))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk}
        ))

        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = (datetime.date.today() +
            datetime.timedelta(weeks=3))

        self.assertEqual(
            response.context['form'].initial['renewal_date'],
            date_3_weeks_in_future
        )

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)

        response = self.client.post(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk,}
        ), {'renewal_date': date_in_future})

        self.assertRedirects(response, reverse('all-borrowed'))

    def test_form_invalid_renewal_date_past(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)

        response = self.client.post(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk}
        ), {'renewal_date': date_in_past})

        self.assertEqual(response.status_code, 200)

        self.assertFormError(
            response.context['form'],
            'renewal_date',
            'Invalid date - renewal in the past'
        )

    def test_form_invalid_renewal_date_future(self):
        self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)

        response = self.client.post(reverse(
            'renew-book-librarian',
            kwargs={'pk': self.test_bookinstance1.pk}
        ), {'renewal_date': date_in_future})

        self.assertEqual(response.status_code, 200)

        self.assertFormError(
            response.context['form'],
            'renewal_date',
            'Invalid date - renewal more than 4 weeks ahead'
        )



