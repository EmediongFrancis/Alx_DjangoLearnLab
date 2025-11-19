from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView

from .models import Book
from .models import Library
from .models import UserProfile


def list_books(request):
    """
    Function-based view that lists all books available in the database.
    Renders a simple text list of book titles and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    including all books available in that library.
    """

    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = (
            self.object.books.select_related("author").all()
        )
        return context


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:book-list')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Role-based access control helper functions
def is_admin(user):
    """Check if user has Admin role."""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'profile') and user.profile.role == 'Admin'


def is_librarian(user):
    """Check if user has Librarian role."""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'profile') and user.profile.role == 'Librarian'


def is_member(user):
    """Check if user has Member role."""
    if not user.is_authenticated:
        return False
    return hasattr(user, 'profile') and user.profile.role == 'Member'


# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """Admin-only view accessible only to users with Admin role."""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian-only view accessible only to users with Librarian role."""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    """Member-only view accessible only to users with Member role."""
    return render(request, 'relationship_app/member_view.html')
