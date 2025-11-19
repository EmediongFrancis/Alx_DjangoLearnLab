# Delete Operation

## Command
```python
from bookshelf.models import Book

# Retrieve the book (using the updated title)
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Number of books remaining: {all_books.count()}")
print("All books:")
for book in all_books:
    print(book)
```

## Expected Output
```
(1, {'bookshelf.Book': 1})
Number of books remaining: 0
All books:
```

## Alternative Delete Method

### Using delete() on QuerySet
```python
# Delete directly without retrieving the object first
Book.objects.filter(title="Nineteen Eighty-Four").delete()

# Confirm deletion
remaining_books = Book.objects.all()
print(f"Books remaining: {remaining_books.count()}")
```

## Expected Output (Alternative Method)
```
(1, {'bookshelf.Book': 1})
Books remaining: 0
```

## Verification Steps

### Try to retrieve the deleted book (will raise exception)
```python
try:
    deleted_book = Book.objects.get(title="Nineteen Eighty-Four")
    print(deleted_book)
except Book.DoesNotExist:
    print("Book not found - deletion confirmed!")
```

## Expected Output (Verification)
```
Book not found - deletion confirmed!
```

## Notes
- The `delete()` method returns a tuple: `(number_of_objects_deleted, {model_name: count})`
- After deletion, the object no longer exists in the database
- Attempting to retrieve a deleted object will raise `DoesNotExist` exception
- The `delete()` method can also be called on a QuerySet to delete multiple objects at once

