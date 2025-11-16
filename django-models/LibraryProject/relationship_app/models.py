from django.db import models


class Author(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book with a foreign key to Author."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author.name}"


class Library(models.Model):
    """Model representing a library with many-to-many relationship to Book."""
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(
        Book,
        related_name='libraries',
        blank=True
    )

    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"
        ordering = ['name']

    def __str__(self):
        return self.name


class Librarian(models.Model):
    """Model representing a librarian with one-to-one relationship to Library."""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name='librarian'
    )

    class Meta:
        verbose_name = "Librarian"
        verbose_name_plural = "Librarians"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.library.name}"
