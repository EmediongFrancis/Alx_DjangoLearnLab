from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView

from .models import Book
from .models import Library


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


# Authentication Views
class CustomLoginView(LoginView):
    """User login view using Django's built-in LoginView."""
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """User logout view using Django's built-in LogoutView."""
    template_name = 'relationship_app/logout.html'
    next_page = None  # Show template instead of redirecting


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
