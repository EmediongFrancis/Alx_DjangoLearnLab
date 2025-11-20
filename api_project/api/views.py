from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer


class BookList(ListAPIView):
    """
    API view to list all books.
    Returns a JSON response containing all book records.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
