from django.shortcuts import render
from django.views.generic import DetailView

from .models import Book
from .models import Library


def book_list_view(request):
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
