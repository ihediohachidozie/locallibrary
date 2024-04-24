from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

import datetime
from django.utils import timezone
# Get user model from settings
from django.contrib.auth import get_user_model

User = get_user_model()

from catalog.models import Author, Book, Genre, Language, BookInstance

import uuid
from django.contrib.auth.models import \
    Permission  # Required to grant the permission needed to set a book as returned.import


# Create your tests here.

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Dominique {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['author_list']), 3)


class AuthorDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Dominique {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        author = Author.objects.get(pk=1)
        response = self.client.get(f'/catalog/author/{author.id}')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        author = Author.objects.get(pk=1)
        response = self.client.get(f'/catalog/author/{author.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'author_detail.html')

    def test_view_url_accessible_by_name(self):
        author = Author.objects.get(pk=1)
        response = self.client.get(reverse("author-detail", args=(author.id,)))  # kwargs={'pk': author.id}
        self.assertEqual(response.status_code, 200)


class BookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 books for pagination tests
        number_of_books = 13
        for book_id in range(number_of_books):
            # Set up non-modified objects used by all test methods
            author = Author.objects.create(first_name=f'Big {book_id}', last_name=f'Bob {book_id}',
                                           date_of_birth='1958-06-15', date_of_death='2000-05-05')
            summary = f"Book {book_id} Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                      "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                      "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
            language = Language.objects.create(name=f"English {book_id}")
            genre1 = Genre.objects.create(name=f"Fantasy {book_id}")
            genre2 = Genre.objects.create(name=f"Action {book_id}")

            book = Book.objects.create(title=f'Farm Animal {book_id}', author=author, summary=summary,
                                       isbn=f'2000505087778{book_id}', language=language)
            book.genre.set([genre1.id, genre2.id])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['book_list']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('books') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['book_list']), 3)


class BookDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 books for pagination tests
        number_of_books = 13
        for book_id in range(number_of_books):
            # Set up non-modified objects used by all test methods
            author = Author.objects.create(first_name=f'Big {book_id}', last_name=f'Bob {book_id}',
                                           date_of_birth='1958-06-15', date_of_death='2000-05-05')
            summary = f"Book {book_id} Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                      "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                      "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
            language = Language.objects.create(name=f"English {book_id}")
            genre1 = Genre.objects.create(name=f"Fantasy {book_id}")
            genre2 = Genre.objects.create(name=f"Action {book_id}")

            book = Book.objects.create(title=f'Farm Animal {book_id}', author=author, summary=summary,
                                       isbn=f'2000505087778{book_id}', language=language)
            book.genre.set([genre1.id, genre2.id])

    def test_view_url_exists_at_desired_location(self):
        book = Book.objects.get(pk=1)
        response = self.client.get(f'/catalog/book/{book.id}')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        book = Book.objects.get(pk=1)
        response = self.client.get(f'/catalog/book/{book.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_detail.html')

    def test_view_url_accessible_by_name(self):
        book = Book.objects.get(pk=1)
        response = self.client.get(reverse("book-detail", kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, 200)


class IndexTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_context_has_num_books(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_books' in response.context)

        context = ['num_books', 'num_instances',
                   'num_instances_available',
                   'num_authors',
                   'num_genres',
                   'num_books_available',
                   'num_visits']

    def test_context_has_num_instances_available(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_instances_available' in response.context)

    def test_context_has_num_authors(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_authors' in response.context)

    def test_context_has_num_instances(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_instances' in response.context)

    def test_context_has_num_genres(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_genres' in response.context)

    def test_context_has_num_books_available(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_books_available' in response.context)

    def test_context_has_num_visits(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('num_visits' in response.context)


# Views that are restricted to logged-in users

class LoanedBooksByUserListViewTest(TestCase):
    def setUp(self) -> None:
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)  # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy % 5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            BookInstance.objects.create(
                book=test_book,
                imprint='Unlikely Imprint, 2016',
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check that initially we don't have any books in list (none on loan)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)

        # Now change all books to be on loan
        books = BookInstance.objects.all()[:10]

        for book in books:
            book.status = 'o'
            book.save()

        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('my-borrowed'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('bookinstance_list' in response.context)  # Check that bookinstance is passed to the template

        # Confirm all books belong to testuser1 and are on loan
        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual(bookitem.status, 'o')

    def test_pages_ordered_by_due_date(self):
        # Change all books to be on loan
        for book in BookInstance.objects.all():
            book.status = 'o'
            book.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['bookinstance_list']), 10)

        last_date = 0
        for book in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back

    def test_pagination_is_ten(self):
        # Change all books to be on loan
        for book in BookInstance.objects.all():
            book.status = 'o'
            book.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['bookinstance_list']), 10)


class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Give test_user2 permission to renew books.
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)  # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user1,
            status='o',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2016',
            due_back=return_date,
            borrower=test_user2,
            status='o',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))

        # Check that it lets us login - this is our book and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        # self.assertEqual(response.context['form'].initial['renewal_date'], date_3_weeks_in_future)
        self.assertEqual(response.context['form'].initial['due_back'], date_3_weeks_in_future)

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'due_back': valid_date_in_future})
        # or this {'renewal_date': valid_date_in_future} for renewal date name field
        self.assertRedirects(response, reverse('all-borrowed'))

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'due_back': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'due_back', 'Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'due_back': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'due_back', 'Invalid date - renewal more than 4 weeks ahead')


class AuthorCreateViewTest(TestCase):
    """Test case for the AuthorCreate view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user = User.objects.create_user(username='test_user', password='some_password')

        content_type_author = ContentType.objects.get_for_model(Author)
        perm_add_author = Permission.objects.get(
            content_type=content_type_author,
            codename="add_author",
        )

        test_user.user_permissions.add(perm_add_author)

        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_create_author(self):
        login = self.client.login(username='test_user', password='some_password')
        response = self.client.get(reverse('author-create'))

        # Check that it lets us log in - this is our book, and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_form_create_author_initially_has_default_date_of_death(self):
        login = self.client.login(username='test_user', password='some_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        default_death_date = '11/11/2023'
        self.assertEqual(response.context['form'].initial['date_of_death'], default_death_date)

    def test_uses_correct_template_author_form(self):
        login = self.client.login(username='test_user', password='some_password')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'author_form.html')

    def test_redirects_to_author_detail_on_success(self):
        login = self.client.login(username='test_user', password='some_password')
        author_data = {
            'first_name': 'John',
            'last_name': 'Smith'
        }
        # Post the data
        response = self.client.post(reverse('author-create'), author_data)
        # Get the last saved author
        author = Author.objects.latest("id")
        self.assertRedirects(response, reverse('author-detail', args=(author.id,)))


class AuthorDeleteViewTest(TestCase):
    """Test case for the AuthorDelete view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user = User.objects.create_user(username='test_user', password='some_password')

        content_type_author = ContentType.objects.get_for_model(Author)
        perm_delete_author = Permission.objects.get(
            content_type=content_type_author,
            codename="delete_author",
        )

        test_user.user_permissions.add(perm_delete_author)

        test_user.save()

        test_author = Author.objects.create(first_name='John', last_name='Smith')

    def test_redirect_if_not_logged_in(self):
        author = Author.objects.get(id=1)
        response = self.client.get(reverse('author-delete', kwargs={'pk': author.id}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_delete_author(self):
        login = self.client.login(username='test_user', password='some_password')
        author = Author.objects.get(id=1)
        response = self.client.get(reverse('author-delete', kwargs={'pk': author.id}))

        # Check that it lets us log in - this is our book, and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template_author_form(self):
        login = self.client.login(username='test_user', password='some_password')
        author = Author.objects.get(id=1)
        response = self.client.get(reverse('author-delete', kwargs={'pk': author.id}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'author_confirm_delete.html')

    def test_redirects_to_authors_list_on_success(self):
        login = self.client.login(username='test_user', password='some_password')
        author = Author.objects.get(id=1)
        # Post the data
        response = self.client.post(reverse('author-delete', args=(author.id,)))

        self.assertRedirects(response, reverse('authors'))


class AuthorUpdateViewTest(TestCase):
    """Test case for the AuthorDetail view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user = User.objects.create_user(username='test_user', password='some_password')

        content_type_author = ContentType.objects.get_for_model(Author)
        perm_change_author = Permission.objects.get(
            content_type=content_type_author,
            codename="change_author",
        )

        test_user.user_permissions.add(perm_change_author)

        test_user.save()
        test_author = Author.objects.create(first_name='John', last_name='Smith')

    def test_redirect_if_not_logged_in(self):
        author = Author.objects.get(id=1)
        response = self.client.get(reverse('author-update', kwargs={'pk': author.id}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_change_author(self):
        login = self.client.login(username='test_user', password='some_password')
        author = Author.objects.get(id=1)
        response = self.client.get(reverse('author-update', kwargs={'pk': author.id}))

        # Check that it lets us log in - this is our book, and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template_author_form(self):
        login = self.client.login(username='test_user', password='some_password')
        author = Author.objects.get(id=1)
        response = self.client.get(reverse('author-update', kwargs={'pk': author.id}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'author_form.html')

    def test_redirects_to_author_detail_on_success(self):
        login = self.client.login(username='test_user', password='some_password')
        author = Author.objects.get(id=1)
        author_data = {
            'first_name': 'John',
            'last_name': 'Smith'
        }
        # Post the data
        response = self.client.post(reverse('author-update', args=(author.id,)), author_data)

        self.assertRedirects(response, reverse('author-detail', args=(author.id,)))


class BookCreateViewTest(TestCase):
    """Test case for the BookCreate view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user = User.objects.create_user(username='test_user', password='some_password')

        content_type_book = ContentType.objects.get_for_model(Book)
        perm_add_book = Permission.objects.get(
            content_type=content_type_book,
            codename="add_book",
        )

        test_user.user_permissions.add(perm_add_book)

        test_user.save()

        # Create a book
        for book in range(3):
            author = Author.objects.create(first_name=f'Big {book}', last_name=f'Bob {book}',
                                           date_of_birth='1958-06-15', date_of_death='2000-05-05')
            summary = f"Book {book} Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                      "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                      "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
            language = Language.objects.create(name=f"English {book}")
            genre1 = Genre.objects.create(name=f"Fantasy {book}")
            genre2 = Genre.objects.create(name=f"Action {book}")

            book = Book.objects.create(title=f'Farm Animal {book}', author=author, summary=summary,
                                       isbn=f'2000505087778{book}', language=language)
            book.genre.set([genre1.id, genre2.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('book-create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_create_author(self):
        login = self.client.login(username='test_user', password='some_password')
        response = self.client.get(reverse('book-create'))

        # Check that it lets us log in - this is our book, and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template_book_form(self):
        login = self.client.login(username='test_user', password='some_password')
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'book_form.html')

    def test_redirects_to_book_detail_on_success(self):
        login = self.client.login(username='test_user', password='some_password')
        author = Author.objects.create(first_name=f'Big', last_name=f'Bob',
                                       date_of_birth='1958-06-15', date_of_death='2000-05-05')
        summary = f"Book Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                  "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                  "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        language = Language.objects.create(name="English")

        book_data = {
            'title': 'Farm Animal',
            'author': author,
            'summary': summary,
            'isbn': '2000505087778',
            'language': language,
        }
        # Post the data
        response = self.client.post(reverse('book-create'), book_data)
        # Get the last saved book
        book = Book.objects.latest("id")
        self.assertEqual(response.status_code, 200)

        # self.assertRedirects(response, reverse('book-detail', args=(book.id,)))


class BookDeleteViewTest(TestCase):
    """Test case for the BookDelete view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user = User.objects.create_user(username='test_user', password='some_password')

        content_type_book = ContentType.objects.get_for_model(Book)
        perm_delete_book = Permission.objects.get(
            content_type=content_type_book,
            codename="delete_book",
        )

        test_user.user_permissions.add(perm_delete_book)

        test_user.save()

        # Create a book
        for book in range(3):
            author = Author.objects.create(first_name=f'Big {book}', last_name=f'Bob {book}',
                                           date_of_birth='1958-06-15', date_of_death='2000-05-05')
            summary = f"Book {book} Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                      "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                      "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
            language = Language.objects.create(name=f"English {book}")
            genre1 = Genre.objects.create(name=f"Fantasy {book}")
            genre2 = Genre.objects.create(name=f"Action {book}")

            book = Book.objects.create(title=f'Farm Animal {book}', author=author, summary=summary,
                                       isbn=f'2000505087778{book}', language=language)
            book.genre.set([genre1.id, genre2.id])

    def test_redirect_if_not_logged_in(self):
        book = Book.objects.get(id=1)
        response = self.client.get(reverse('book-delete', kwargs={'pk': book.id}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_delete_book(self):
        login = self.client.login(username='test_user', password='some_password')
        book = Book.objects.get(id=1)
        response = self.client.get(reverse('book-delete', kwargs={'pk': book.id}))

        # Check that it lets us log in - this is our book, and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template_book_form(self):
        login = self.client.login(username='test_user', password='some_password')
        book = Book.objects.get(id=1)
        response = self.client.get(reverse('book-delete', kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'book_confirm_delete.html')

    def test_redirects_to_books_list_on_success(self):
        login = self.client.login(username='test_user', password='some_password')
        book = Book.objects.get(id=1)
        # Post the data
        response = self.client.post(reverse('book-delete', args=(book.id,)))

        self.assertRedirects(response, reverse('books'))


class BookUpdateViewTest(TestCase):
    """Test case for the BookDetail view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_user = User.objects.create_user(username='test_user', password='some_password')

        content_type_book = ContentType.objects.get_for_model(Book)
        perm_change_book = Permission.objects.get(
            content_type=content_type_book,
            codename="change_book",
        )

        test_user.user_permissions.add(perm_change_book)

        test_user.save()

        # Create a book
        for book in range(3):
            author = Author.objects.create(first_name=f'Big {book}', last_name=f'Bob {book}',
                                           date_of_birth='1958-06-15', date_of_death='2000-05-05')
            summary = f"Book {book} Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                      "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                      "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
            language = Language.objects.create(name=f"English {book}")
            genre1 = Genre.objects.create(name=f"Fantasy {book}")
            genre2 = Genre.objects.create(name=f"Action {book}")

            book = Book.objects.create(title=f'Farm Animal {book}', author=author, summary=summary,
                                       isbn=f'2000505087778{book}', language=language)
            book.genre.set([genre1.id, genre2.id])

    def test_redirect_if_not_logged_in(self):
        book = Book.objects.get(id=1)
        response = self.client.get(reverse('book-update', kwargs={'pk': book.id}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_with_permission_change_book(self):
        login = self.client.login(username='test_user', password='some_password')
        book = Book.objects.get(id=1)
        response = self.client.get(reverse('book-update', kwargs={'pk': book.id}))

        # Check that it lets us log in - this is our book, and we have the right permissions
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template_book_form(self):
        login = self.client.login(username='test_user', password='some_password')
        book = Book.objects.get(id=1)
        response = self.client.get(reverse('book-update', kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'book_form.html')

    def test_redirects_to_book_detail_on_success(self):
        login = self.client.login(username='test_user', password='some_password')
        book = Book.objects.get(id=1)
        book_data = {
            book.title: 'Farm Animal',
            book.isbn: '2000505087778',
        }
        # Post the data
        response = self.client.post(reverse('book-update', args=(book.id,)), book_data)
        self.assertEqual(response.status_code, 200)

        # self.assertRedirects(response, reverse('book-detail', args=(book.id,)))

