from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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


class Book(models.Model):
    """Book model with custom permissions for access control."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']
        # Custom permissions for access control
        permissions = (
            ("can_view", "Can view book records"),
            ("can_create", "Can create book records"),
            ("can_edit", "Can edit book records"),
            ("can_delete", "Can delete book records"),
        )

    def __str__(self):
        return f"{self.title} by {self.author}"