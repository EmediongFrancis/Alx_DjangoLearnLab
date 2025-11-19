# Permissions and Groups Setup Guide

This document explains how permissions and groups are configured and used in the bookshelf application.

## Overview

The bookshelf application implements a role-based access control system using Django's built-in permissions and groups. This allows fine-grained control over who can view, create, edit, or delete book records.

## Custom Permissions

The `Book` model defines four custom permissions:

- **can_view**: Allows users to view book records
- **can_create**: Allows users to create new book records
- **can_edit**: Allows users to edit existing book records
- **can_delete**: Allows users to delete book records

These permissions are defined in the `Book` model's `Meta` class:

```python
class Meta:
    permissions = (
        ("can_view", "Can view book records"),
        ("can_create", "Can create book records"),
        ("can_edit", "Can edit book records"),
        ("can_delete", "Can delete book records"),
    )
```

## User Groups

Three groups are set up with different permission levels:

### 1. Viewers
- **Permissions**: `can_view`
- **Capabilities**: Can only view book records
- **Use Case**: Regular users who should only be able to browse books

### 2. Editors
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Capabilities**: Can view, create, and edit books, but cannot delete
- **Use Case**: Content managers who maintain the book catalog

### 3. Admins
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Capabilities**: Full access to all book operations
- **Use Case**: Administrators who need complete control

## Setting Up Groups

### Automatic Setup (Recommended)

Run the management command to automatically create groups and assign permissions:

```bash
python manage.py setup_groups
```

This command will:
1. Create the three groups (Viewers, Editors, Admins) if they don't exist
2. Assign appropriate permissions to each group
3. Display a confirmation message

### Manual Setup via Django Admin

1. Navigate to Django Admin: `http://localhost:8000/admin/`
2. Go to **Authentication and Authorization** → **Groups**
3. Create groups manually:
   - Click "Add Group"
   - Enter group name (Viewers, Editors, or Admins)
   - Select the appropriate permissions from the "Available permissions" list
   - Click "Save"

## Assigning Users to Groups

### Via Django Admin

1. Navigate to **Authentication and Authorization** → **Users**
2. Click on a user to edit
3. Scroll to the "Groups" section
4. Select one or more groups from the "Available groups" list
5. Click "Save"

### Via Django Shell

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()
user = User.objects.get(username='username')
group = Group.objects.get(name='Editors')
user.groups.add(group)
```

## Permission Enforcement in Views

All views use the `@permission_required` decorator to enforce permissions:

```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View implementation
    pass
```

### View Permissions

- **book_list**: Requires `can_view`
- **book_detail**: Requires `can_view`
- **book_create**: Requires `can_create`
- **book_edit**: Requires `can_edit`
- **book_delete**: Requires `can_delete`

If a user tries to access a view without the required permission, Django will raise a `PermissionDenied` exception (HTTP 403).

## Testing Permissions

### Step 1: Create Test Users

```python
from django.contrib.auth import get_user_model

User = get_user_model()

# Create a viewer
viewer = User.objects.create_user(
    username='viewer',
    email='viewer@example.com',
    password='testpass123'
)

# Create an editor
editor = User.objects.create_user(
    username='editor',
    email='editor@example.com',
    password='testpass123'
)

# Create an admin
admin = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='testpass123'
)
```

### Step 2: Assign Users to Groups

```python
from django.contrib.auth.models import Group

viewers_group = Group.objects.get(name='Viewers')
editors_group = Group.objects.get(name='Editors')
admins_group = Group.objects.get(name='Admins')

viewer.groups.add(viewers_group)
editor.groups.add(editors_group)
admin.groups.add(admins_group)
```

### Step 3: Test Access

1. Log in as each user
2. Try to access different views:
   - **Viewer**: Should only be able to view books
   - **Editor**: Should be able to view, create, and edit books
   - **Admin**: Should have full access including delete

## URL Patterns

All book-related views are accessible at:

- `/books/` - List all books (requires `can_view`)
- `/books/<id>/` - View book details (requires `can_view`)
- `/books/create/` - Create new book (requires `can_create`)
- `/books/<id>/edit/` - Edit book (requires `can_edit`)
- `/books/<id>/delete/` - Delete book (requires `can_delete`)

## Template Permission Checks

Templates can check permissions using the `perms` template variable:

```django
{% if perms.bookshelf.can_create %}
    <a href="{% url 'bookshelf:book-create' %}">Create New Book</a>
{% endif %}
```

This allows conditional display of UI elements based on user permissions.

## Important Notes

1. **Superusers**: Users with `is_superuser=True` automatically have all permissions and can bypass permission checks.

2. **Permission Names**: Permission codenames follow the pattern `app_label.permission_codename` (e.g., `bookshelf.can_view`).

3. **Migrations**: After adding custom permissions, run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Group Updates**: If you modify permissions in the model, re-run `setup_groups` to update group permissions.

## Troubleshooting

### Permission Denied Errors

If users are getting 403 errors:
1. Verify the user is assigned to the correct group
2. Check that the group has the required permissions
3. Ensure migrations have been run after adding permissions

### Groups Not Created

If groups don't exist:
1. Run `python manage.py setup_groups`
2. Or create them manually via Django Admin

### Permissions Not Working

1. Verify the permission codename matches exactly (case-sensitive)
2. Check that the user is logged in
3. Ensure the user's group has the permission assigned

