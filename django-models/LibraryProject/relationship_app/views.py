from django.http import HttpResponse
from django.views.generic import DetailView

from .models import Book, Library


def book_list_view(request):
    """
    Function-based view that lists all books available in the database.
    Returns a plain text response containing each book title and author.
    """
    books = Book.objects.select_related("author").all()

    if not books.exists():
        content = "No books available."
    else:
        lines = [
            f"{book.title} by {book.author.name if book.author else 'Unknown Author'}"
            for book in books
        ]
        content = "\n".join(lines)

    return HttpResponse(content, content_type="text/plain")


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
