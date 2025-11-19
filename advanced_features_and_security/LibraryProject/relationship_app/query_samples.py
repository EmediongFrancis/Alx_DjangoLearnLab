"""
Django ORM Query Samples for Relationship Models

This script demonstrates how to query models with different relationship types:
- ForeignKey: Book to Author
- ManyToManyField: Library to Book
- OneToOneField: Librarian to Library

To run this script:
    python manage.py shell < query_samples.py
    OR
    python manage.py shell
    >>> exec(open('relationship_app/query_samples.py').read())
"""

import os
import django

# Setup Django environment (if running as standalone script)
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
    django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author():
    """
    Query 1: ForeignKey Relationship
    Get all books by a specific author.
    
    This demonstrates the ForeignKey relationship from Book to Author.
    """
    print("=" * 60)
    print("QUERY 1: Query all books by a specific author (ForeignKey)")
    print("=" * 60)
    
    # Method 1: Using filter on the Book model
    author_name = "George Orwell"
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        
        print(f"\nMethod 1: Using filter()")
        print(f"Author: {author_name}")
        print(f"Number of books: {books.count()}")
        print("Books:")
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        print("Creating sample data for demonstration...")
        author = Author.objects.create(name=author_name)
        Book.objects.create(title="1984", author=author)
        Book.objects.create(title="Animal Farm", author=author)
        books = Book.objects.filter(author=author)
        print(f"\nAuthor: {author_name}")
        print(f"Number of books: {books.count()}")
        print("Books:")
        for book in books:
            print(f"  - {book.title}")
    
    # Method 2: Using the reverse relationship (related_name='books')
    print(f"\nMethod 2: Using reverse relationship (author.books)")
    print(f"Author: {author.name}")
    print(f"Number of books: {author.books.count()}")
    print("Books:")
    for book in author.books.all():
        print(f"  - {book.title}")
    
    # Method 3: Using __lookup for direct filtering
    print(f"\nMethod 3: Using __lookup (Book.objects.filter(author__name=...))")
    books_by_lookup = Book.objects.filter(author__name=author_name)
    print(f"Number of books: {books_by_lookup.count()}")
    print("Books:")
    for book in books_by_lookup:
        print(f"  - {book.title}")
    
    print("\n" + "-" * 60 + "\n")


def list_books_in_library():
    """
    Query 2: ManyToManyField Relationship
    List all books in a library.
    
    This demonstrates the ManyToManyField relationship from Library to Book.
    """
    print("=" * 60)
    print("QUERY 2: List all books in a library (ManyToManyField)")
    print("=" * 60)
    
    library_name = "Central Library"
    
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        print("Creating sample data for demonstration...")
        library = Library.objects.create(name=library_name)
        
        # Get or create some books
        author = Author.objects.first()
        if not author:
            author = Author.objects.create(name="Sample Author")
        
        book1, _ = Book.objects.get_or_create(
            title="Sample Book 1",
            defaults={'author': author}
        )
        book2, _ = Book.objects.get_or_create(
            title="Sample Book 2",
            defaults={'author': author}
        )
        
        # Add books to library
        library.books.add(book1, book2)
    
    # Method 1: Direct access through the ManyToManyField
    print(f"\nMethod 1: Direct access (library.books.all())")
    print(f"Library: {library.name}")
    books = library.books.all()
    print(f"Number of books: {books.count()}")
    print("Books in library:")
    for book in books:
        print(f"  - {book.title} by {book.author.name}")
    
    # Method 2: Using filter with __lookup
    print(f"\nMethod 2: Using filter with __lookup")
    books_in_library = Book.objects.filter(libraries__name=library_name)
    print(f"Library: {library_name}")
    print(f"Number of books: {books_in_library.count()}")
    print("Books in library:")
    for book in books_in_library:
        print(f"  - {book.title} by {book.author.name}")
    
    # Method 3: Using the reverse relationship (related_name='libraries')
    if books.exists():
        first_book = books.first()
        print(f"\nMethod 3: Using reverse relationship (book.libraries.all())")
        print(f"Book: {first_book.title}")
        libraries_with_book = first_book.libraries.all()
        print(f"Number of libraries containing this book: {libraries_with_book.count()}")
        print("Libraries:")
        for lib in libraries_with_book:
            print(f"  - {lib.name}")
    
    print("\n" + "-" * 60 + "\n")


def retrieve_librarian_for_library():
    """
    Query 3: OneToOneField Relationship
    Retrieve the librarian for a library.
    
    This demonstrates the OneToOneField relationship from Librarian to Library.
    """
    print("=" * 60)
    print("QUERY 3: Retrieve the librarian for a library (OneToOneField)")
    print("=" * 60)
    
    library_name = "Central Library"
    
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        print("Creating sample data for demonstration...")
        library = Library.objects.create(name=library_name)
    
    # Method 1: Using the reverse relationship (related_name='librarian')
    print(f"\nMethod 1: Using reverse relationship (library.librarian)")
    print(f"Library: {library.name}")
    try:
        librarian = library.librarian
        print(f"Librarian: {librarian.name}")
        print(f"Librarian ID: {librarian.id}")
    except Librarian.DoesNotExist:
        print("No librarian assigned to this library.")
        print("Creating sample librarian...")
        librarian = Librarian.objects.create(
            name="John Doe",
            library=library
        )
        print(f"Created librarian: {librarian.name}")
    
    # Method 2: Direct query on Librarian model
    print(f"\nMethod 2: Direct query (Librarian.objects.get(library=...))")
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"Library: {library.name}")
        print(f"Librarian: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library.name}")
    
    # Method 3: Using __lookup
    print(f"\nMethod 3: Using __lookup (Librarian.objects.filter(library__name=...))")
    librarians = Librarian.objects.filter(library__name=library_name)
    if librarians.exists():
        librarian = librarians.first()
        print(f"Library: {library_name}")
        print(f"Librarian: {librarian.name}")
    else:
        print(f"No librarian found for {library_name}")
    
    # Method 4: Accessing library from librarian (forward relationship)
    if Librarian.objects.exists():
        librarian = Librarian.objects.first()
        print(f"\nMethod 4: Forward relationship (librarian.library)")
        print(f"Librarian: {librarian.name}")
        print(f"Library: {librarian.library.name}")
    
    print("\n" + "-" * 60 + "\n")


def main():
    """Run all query examples."""
    print("\n" + "=" * 60)
    print("DJANGO ORM RELATIONSHIP QUERY SAMPLES")
    print("=" * 60 + "\n")
    
    # Execute all query examples
    query_books_by_author()
    list_books_in_library()
    retrieve_librarian_for_library()
    
    print("=" * 60)
    print("All queries completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
else:
    # If imported in Django shell, just define functions
    # User can call them individually
    pass

