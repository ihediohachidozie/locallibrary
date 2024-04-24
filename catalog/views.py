from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from catalog.forms import RenewBookForm, RenewBookModelForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Author, Book


# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Challenge
    num_genres = Genre.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_books_available = Book.objects.filter(title__icontains='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_available': num_books_available,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # your own name for the list as a template variable

    def get_queryset(self):
        return Book.objects.all()  # Get ALl books

    # queryset = Book.objects.filter(title__incontains='war')[:5]  # Get 5 books containing the title war
    template_name = 'book_list.html'  # Specify your own template name/location
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'  # your own name for the list as a template variable

    def get_queryset(self):
        return Author.objects.all()  # Get all author

    template_name = 'author_list.html'  # Specify the template name
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class AllBorrowedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books borrowed with restricted view to staff members only."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'bookinstance_list_all_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        form1 = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form1.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.due_back = form1.cleaned_data['due_back']

            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        form1 = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form1,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'
    template_name = 'author_form.html'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'
    template_name = 'author_form.html'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'
    template_name = 'author_confirm_delete.html'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('author-delete', kwargs={'pk': self.object.pk})
            )


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.add_book'
    template_name = 'book_form.html'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.change_book'
    template_name = 'book_form.html'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'
    template_name = 'book_confirm_delete.html'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('book-delete', kwargs={'pk': self.object.pk})
            )

