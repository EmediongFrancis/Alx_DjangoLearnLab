from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Custom User Manager
class CustomUserManager(BaseUserManager):
    """Custom user manager for CustomUser model."""
    
    def create_user(self, email, username, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        """Create and save a regular user with the given email, username, and password."""
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        """Create and save a superuser with the given email, username, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(
            email=email,
            username=username,
            password=password,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )


# Custom User Model
class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        verbose_name="Profile Photo"
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']
    
    def __str__(self):
        return self.username


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
    """Model extending CustomUser with role-based access control."""
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(
        'CustomUser',
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


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to automatically create UserProfile when a CustomUser is created."""
    if created:
        UserProfile.objects.create(user=instance, role='Member')


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Signal to save UserProfile when CustomUser is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance, role='Member')
