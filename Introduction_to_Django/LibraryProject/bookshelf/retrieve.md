# Retrieve Operation

## Command
```python
from bookshelf.models import Book

# Retrieve the book we just created
book = Book.objects.get(title="1984")

# Display all attributes
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output
```
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Alternative Retrieval Methods

### Get all books
```python
all_books = Book.objects.all()
for book in all_books:
    print(f"{book.title} by {book.author} ({book.publication_year})")
```

### Filter books
```python
# Get books by a specific author
orwell_books = Book.objects.filter(author="George Orwell")
for book in orwell_books:
    print(book)
```

## Notes
- `get()` returns a single object and raises an exception if no object or multiple objects are found
- `all()` returns a QuerySet containing all objects
- `filter()` returns a QuerySet containing objects matching the given criteria

