"""
Secure views for the bookshelf application.

All views use Django's ORM for database queries, which automatically
parameterizes queries to prevent SQL injection attacks. User inputs are
validated using Django forms to ensure data integrity and security.
"""

from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape

from .forms import BookForm, BookSearchForm, ExampleForm
from .models import Book


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books with secure search functionality.
    Requires 'can_view' permission.
    
    Security features:
    - Uses Django ORM (parameterized queries) to prevent SQL injection
    - Validates search input using Django forms
    - Escapes user input in templates to prevent XSS
    """
    books = Book.objects.all()
    search_form = BookSearchForm(request.GET)
    
    # Secure search using Django ORM - prevents SQL injection
    # Using Q objects for safe query construction
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            # Use ORM filter with Q objects - automatically parameterized
            # This prevents SQL injection by using parameterized queries
            books = books.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
    
    context = {
        'books': books,
        'search_form': search_form,
    }
    return render(request, 'bookshelf/book_list.html', context)


@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    View to display a single book's details.
    Requires 'can_view' permission.
    
    Security features:
    - Uses get_object_or_404 to safely retrieve objects
    - Django templates automatically escape output to prevent XSS
    """
    # get_object_or_404 safely handles invalid IDs and prevents errors
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book using secure form validation.
    Requires 'can_create' permission.
    
    Security features:
    - Uses Django forms for input validation and sanitization
    - CSRF protection via {% csrf_token %} in template
    - Django ORM prevents SQL injection
    - Form validation prevents invalid data
    """
    if request.method == 'POST':
        # Use Django form instead of direct POST access
        # This validates, sanitizes, and escapes user input
        form = BookForm(request.POST)
        if form.is_valid():
            # form.save() uses parameterized queries via ORM
            # All input is validated and sanitized by the form
            book = form.save()
            return redirect('bookshelf:book-detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'action': 'Create'
    })


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book using secure form validation.
    Requires 'can_edit' permission.
    
    Security features:
    - Uses Django forms for input validation
    - CSRF protection via {% csrf_token %} in template
    - Django ORM prevents SQL injection
    - Form validation ensures data integrity
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Use Django form with instance for updates
        # This validates and sanitizes all input
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # form.save() uses parameterized queries and validated data
            book = form.save()
            return redirect('bookshelf:book-detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'action': 'Edit'
    })


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book.
    Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:book-list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
