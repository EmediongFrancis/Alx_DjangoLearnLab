from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import Book, CustomUser


# Custom User Admin
class CustomUserAdmin(BaseUserAdmin):
    """Admin interface for CustomUser model."""
    
    list_display = ('username', 'email', 'date_of_birth', 'profile_photo_display', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    def profile_photo_display(self, obj):
        """Display profile photo thumbnail in admin list."""
        if obj.profile_photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.profile_photo.url
            )
        return "No photo"
    profile_photo_display.short_description = 'Profile Photo'


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Book model.
    Provides enhanced display, filtering, and search capabilities.
    """
    
    # Display fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Enable filtering by author and publication year
    list_filter = ('author', 'publication_year')
    
    # Enable search functionality for title and author
    search_fields = ('title', 'author')
    
    # Default ordering by title (ascending)
    ordering = ('title',)
    
    # Number of items per page in the admin list view
    list_per_page = 25
    
    # Fields to display in the detail/edit form
    fields = ('title', 'author', 'publication_year')

