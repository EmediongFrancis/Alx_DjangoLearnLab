"""
Django forms for the bookshelf application.

These forms provide secure input validation and sanitization to prevent
SQL injection and other security vulnerabilities. Using Django forms ensures
that all user inputs are properly validated and escaped.
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    
    This form uses Django's ModelForm which automatically:
    - Validates input data types
    - Escapes user input to prevent XSS attacks
    - Uses parameterized queries (via ORM) to prevent SQL injection
    - Provides built-in CSRF protection when used with {% csrf_token %}
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'required': True
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'max': '9999',
                'required': True
            }),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'publication_year': 'Publication Year',
        }
        help_texts = {
            'publication_year': 'Enter a valid year (e.g., 2024)',
        }
    
    def clean_title(self):
        """
        Custom validation for title field.
        Sanitizes and validates the title input.
        """
        title = self.cleaned_data.get('title')
        if title:
            # Strip whitespace
            title = title.strip()
            # Check for minimum length
            if len(title) < 2:
                raise ValidationError('Title must be at least 2 characters long.')
            # Check for maximum length (enforced by model, but double-check here)
            if len(title) > 200:
                raise ValidationError('Title must be 200 characters or less.')
        return title
    
    def clean_author(self):
        """
        Custom validation for author field.
        Sanitizes and validates the author input.
        """
        author = self.cleaned_data.get('author')
        if author:
            # Strip whitespace
            author = author.strip()
            # Check for minimum length
            if len(author) < 2:
                raise ValidationError('Author name must be at least 2 characters long.')
            # Check for maximum length
            if len(author) > 100:
                raise ValidationError('Author name must be 100 characters or less.')
        return author
    
    def clean_publication_year(self):
        """
        Custom validation for publication_year field.
        Ensures the year is within a reasonable range.
        """
        publication_year = self.cleaned_data.get('publication_year')
        if publication_year:
            # Validate year range (1000 to current year + 10 for future books)
            from datetime import datetime
            current_year = datetime.now().year
            if publication_year < 1000 or publication_year > current_year + 10:
                raise ValidationError(
                    f'Publication year must be between 1000 and {current_year + 10}.'
                )
        return publication_year
    
    def clean(self):
        """
        Form-level validation.
        Can be used to validate relationships between fields.
        """
        cleaned_data = super().clean()
        # Additional cross-field validation can be added here if needed
        return cleaned_data


class BookSearchForm(forms.Form):
    """
    Form for searching books.
    
    This form demonstrates secure search functionality using Django's ORM
    instead of raw SQL queries, preventing SQL injection attacks.
    """
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or author...'
        }),
        label='Search',
        help_text='Enter a book title or author name to search'
    )
    
    def clean_query(self):
        """
        Sanitize search query input.
        """
        query = self.cleaned_data.get('query', '')
        if query:
            # Strip whitespace and limit length
            query = query.strip()[:200]
        return query


class ExampleForm(forms.Form):
    """
    Example form demonstrating secure input handling and validation.
    """

    name = forms.CharField(
        max_length=100,
        required=True,
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Your full name'}),
        help_text='Enter your full name (required).'
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        help_text='We will never share your email.'
    )
    message = forms.CharField(
        required=False,
        label='Message',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional message'}),
        help_text='Optional: add any notes or questions.'
    )

    def clean_name(self):
        """
        Sanitize and validate the name field.
        """
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        return name

    def clean_message(self):
        """
        Sanitize the optional message field.
        """
        message = self.cleaned_data.get('message', '')
        # Strip leading/trailing whitespace to prevent accidental spaces
        return message.strip()
