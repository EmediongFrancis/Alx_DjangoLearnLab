from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books.
    Returns a JSON response containing all book records.
    
    Authentication: Required (Token or Session)
    Permissions: IsAuthenticated - Any authenticated user can view books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling all CRUD operations on Book model.
    
    Provides the following actions:
    - list: GET /books_all/ - List all books (requires authentication)
    - create: POST /books_all/ - Create a new book (requires authentication)
    - retrieve: GET /books_all/<id>/ - Retrieve a specific book (requires authentication)
    - update: PUT /books_all/<id>/ - Update a book (requires admin)
    - partial_update: PATCH /books_all/<id>/ - Partially update a book (requires admin)
    - destroy: DELETE /books_all/<id>/ - Delete a book (requires admin)
    
    Authentication: Required (Token or Session)
    Permissions:
    - Read operations (list, retrieve): IsAuthenticated - Any authenticated user
    - Write operations (create, update, delete): IsAdminUser - Only admin users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Override get_permissions to apply different permissions based on action.
        - Read operations (list, retrieve): Any authenticated user
        - Write operations (create, update, destroy): Admin users only
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Write operations require admin privileges
            return [IsAdminUser()]
        # Read operations only require authentication
        return [IsAuthenticated()]
