from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books.
    Returns a JSON response containing all book records.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
