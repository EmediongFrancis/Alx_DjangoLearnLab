from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books.
    Returns a JSON response containing all book records.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(ModelViewSet):
    """
    ViewSet for handling all CRUD operations on Book model.
    
    Provides the following actions:
    - list: GET /books_all/ - List all books
    - create: POST /books_all/ - Create a new book
    - retrieve: GET /books_all/<id>/ - Retrieve a specific book
    - update: PUT /books_all/<id>/ - Update a book (full update)
    - partial_update: PATCH /books_all/<id>/ - Partially update a book
    - destroy: DELETE /books_all/<id>/ - Delete a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
