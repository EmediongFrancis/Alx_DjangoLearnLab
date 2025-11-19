from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import Author, Book, CustomUser, Library, Librarian, UserProfile


# Custom User Admin
@admin.register(CustomUser)
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


# UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    list_display = ('user', 'role', 'get_email', 'get_date_of_birth')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)
    
    def get_email(self, obj):
        """Display user email."""
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_date_of_birth(self, obj):
        """Display user date of birth."""
        return obj.user.date_of_birth
    get_date_of_birth.short_description = 'Date of Birth'


# Other model admins
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_book_count')
    search_fields = ('name',)
    filter_horizontal = ('books',)
    
    def get_book_count(self, obj):
        """Display number of books in library."""
        return obj.books.count()
    get_book_count.short_description = 'Number of Books'


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
    list_filter = ('library',)
    search_fields = ('name', 'library__name')
