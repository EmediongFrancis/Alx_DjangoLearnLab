from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        permissions = (
            ("can_add_book", "Can add book records"),
            ("can_change_book", "Can edit book records"),
            ("can_delete_book", "Can delete book records"),
        )

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


class UserProfile(models.Model):
    """Model extending User with role-based access control."""
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Member'
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} - {self.role}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to automatically create UserProfile when a User is created."""
    if created:
        UserProfile.objects.create(user=instance, role='Member')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal to save UserProfile when User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance, role='Member')
