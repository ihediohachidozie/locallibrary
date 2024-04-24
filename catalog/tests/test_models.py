import datetime
import uuid

from django.test import TestCase
from django.utils import timezone

from catalog.models import Author, Language, Genre, Book, BookInstance


# Create your tests here.

# class BookSetUp:
#     author = Author.objects.create(first_name='Big', last_name='Bob', date_of_birth='1958-06-15',
#                                    date_of_death='2000-05-05')
#     summary = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
#               "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
#               "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
#     language = Language.objects.create(name="French")
#     genre1 = Genre.objects.create(name="Fantasy")
#     genre2 = Genre.objects.create(name="Action")
#     genre = Genre.objects.filter(name__in=[genre1.name, genre2.name])
#     book = Book.objects.create(title='Farm Animal', author=author, summary=summary, isbn='2000505087778',
#                                language=language)
#     book.genre.set(genre)
#
#     # return book


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob', date_of_birth='1958-06-15', date_of_death='2000-05-05')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')

    def test_date_of_death_gt_date_of_birth(self):
        author = Author.objects.get(id=1)
        self.assertGreater(author.date_of_death, author.date_of_birth)

    def test_date_of_birth_gt_date_of_death_failed(self):
        author = Author.objects.get(id=1)
        author.date_of_birth = '2024-05-05'
        author.date_of_death = '1958-01-01'
        self.assertFalse(author.date_of_birth < author.date_of_death)


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Language.objects.create(name="English")

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        language = Language.objects.get(id=1)
        expected_object_name = f'{language.name}'
        self.assertEqual(str(language), expected_object_name)

    def test_get_absolute_url(self):
        pass
        # language = Language.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        # self.assertEqual(language.get_absolute_url(), '/catalog/language/1')


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Genre.objects.create(name="Horror")

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        genre = Genre.objects.get(id=1)
        expected_object_name = f'{genre.name}'
        self.assertEqual(str(genre), expected_object_name)

    def test_get_absolute_url(self):
        pass
        # genre = Genre.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        # self.assertEqual(genre.get_absolute_url(), '/catalog/genre/1')


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        author = Author.objects.create(first_name='Big', last_name='Bob', date_of_birth='1958-06-15',
                                       date_of_death='2000-05-05')
        summary = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                  "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                  "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        language = Language.objects.create(name="English")
        genre1 = Genre.objects.create(name="Fantasy")
        genre2 = Genre.objects.create(name="Action")

        book = Book.objects.create(title='Farm Animal', author=author, summary=summary, isbn='2000505087778',
                                   language=language)
        book.genre.set([genre1.id, genre2.id])

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_summary_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_genre_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label, 'genre')

    def test_language_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_summary_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_object_name_is_title(self):
        book = Book.objects.get(id=1)
        expected_object_name = f'{book.title}'
        self.assertEqual(str(book), expected_object_name)

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(book.get_absolute_url(), '/catalog/book/1')


class BookInstanceModelTest(TestCase):
    bookinst = str(uuid.uuid4())
    # book = BookSetUp.book

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        author = Author.objects.create(first_name='Big', last_name='Bob', date_of_birth='1958-06-15',
                                       date_of_death='2000-05-05')
        summary = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                  "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                  "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        language = Language.objects.create(name="English")
        genre1 = Genre.objects.create(name="Fantasy")
        genre2 = Genre.objects.create(name="Action")

        book = Book.objects.create(title='Farm Animal', author=author, summary=summary, isbn='2000505087778',
                                   language=language)
        book.genre.set([genre1.id, genre2.id])
        BookInstance.objects.create(id=cls.bookinst, book=book,
                                    imprint="printed", due_back=date, status='o')

    def test_book_label(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        field_label = bookinstance._meta.get_field('book').verbose_name
        self.assertEqual(field_label, 'book')

    def test_imprint_label(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        field_label = bookinstance._meta.get_field('imprint').verbose_name
        self.assertEqual(field_label, 'imprint')

    def test_due_back_label(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        field_label = bookinstance._meta.get_field('due_back').verbose_name
        self.assertEqual(field_label, 'due back')

    def test_status_label(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        field_label = bookinstance._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_imprint_max_length(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        max_length = bookinstance._meta.get_field('imprint').max_length
        self.assertEqual(max_length, 200)

    def test_status_max_length(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        max_length = bookinstance._meta.get_field('status').max_length
        self.assertEqual(max_length, 1)

    def test_object_name_is_id_book_title(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        expected_object_name = f'{bookinstance.id} ({bookinstance.book.title})'
        self.assertEqual(str(bookinstance), expected_object_name)

    def test_is_overdue_false(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        # This will also fail if the book is overdue.
        self.assertFalse(bookinstance.is_overdue)

    def test_is_overdue_true(self):
        bookinstance = BookInstance.objects.get(id=self.bookinst)
        bookinstance.due_back = datetime.date.today() - datetime.timedelta(days=1)
        # This will also fail if the book is overdue.
        self.assertTrue(bookinstance.is_overdue)
        