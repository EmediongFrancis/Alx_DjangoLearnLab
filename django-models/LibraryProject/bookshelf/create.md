# Create Operation

## Command
```python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
```

## Expected Output
```
# The book object is created and returned
# You can verify by printing the book:
>>> print(book)
1984 by George Orwell

# Access individual attributes:
>>> print(book.id)
1

>>> print(book.title)
1984

>>> print(book.author)
George Orwell

>>> print(book.publication_year)
1949
```

## Notes
- The `create()` method creates and saves the object in a single step
- Django automatically assigns an `id` (primary key) to the new book
- The `__str__` method returns "1984 by George Orwell" when the object is printed

