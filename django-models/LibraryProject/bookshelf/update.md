# Update Operation

## Command
```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"

# Save the changes
book.save()

# Verify the update
print(f"Updated title: {book.title}")
print(book)
```

## Expected Output
```
Updated title: Nineteen Eighty-Four
Nineteen Eighty-Four by George Orwell
```

## Alternative Update Method

### Using update() on QuerySet
```python
# Update directly without retrieving the object first
Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")

# Verify the update
updated_book = Book.objects.get(title="Nineteen Eighty-Four")
print(updated_book)
```

## Expected Output (Alternative Method)
```
Nineteen Eighty-Four by George Orwell
```

## Notes
- When updating an existing object, modify the attribute and call `save()`
- The `update()` method can update multiple objects at once and is more efficient for bulk updates
- Always call `save()` after modifying object attributes to persist changes to the database

