# API Authentication and Permissions Guide

This document explains how authentication and permissions are configured for the API endpoints.

## Overview

The API uses **Token Authentication** to secure endpoints. Users must obtain an authentication token and include it in their requests to access protected endpoints.

## Authentication Setup

### Token Authentication

Token authentication is configured in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Getting an Authentication Token

#### Step 1: Obtain a Token

Send a POST request to `/api/token/` with your username and password:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### Step 2: Use the Token in Requests

Include the token in the `Authorization` header of your requests:

```bash
curl http://localhost:8000/api/books_all/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## Permission Classes

### BookList View

- **Permission**: `IsAuthenticated`
- **Access**: Any authenticated user can view the list of books
- **Endpoint**: `GET /api/books/`

### BookViewSet

The ViewSet uses different permissions based on the action:

#### Read Operations (List and Retrieve)
- **Permission**: `IsAuthenticated`
- **Access**: Any authenticated user
- **Endpoints**:
  - `GET /api/books_all/` - List all books
  - `GET /api/books_all/<id>/` - Retrieve a specific book

#### Write Operations (Create, Update, Delete)
- **Permission**: `IsAdminUser`
- **Access**: Only users with `is_staff=True` (admin users)
- **Endpoints**:
  - `POST /api/books_all/` - Create a new book
  - `PUT /api/books_all/<id>/` - Update a book (full update)
  - `PATCH /api/books_all/<id>/` - Partially update a book
  - `DELETE /api/books_all/<id>/` - Delete a book

## Setting Up Users

### Create a Regular User

```python
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.create_user(
    username='regular_user',
    password='password123',
    email='user@example.com'
)
```

### Create an Admin User

```python
from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.create_user(
    username='admin_user',
    password='admin123',
    email='admin@example.com',
    is_staff=True  # Required for admin permissions
)
```

Or use Django's management command:

```bash
python manage.py createsuperuser
```

### Generate Token for Existing User

You can generate a token for an existing user via Django shell:

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='your_username')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
```

## Testing Authentication

### Test Without Token (Should Fail)

```bash
curl http://localhost:8000/api/books_all/
```

**Expected Response:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Test With Token (Should Succeed)

```bash
# First, get a token
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}' \
  | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# Use the token to access the API
curl http://localhost:8000/api/books_all/ \
  -H "Authorization: Token $TOKEN"
```

### Test Admin-Only Operations

Regular users can read but cannot create/update/delete:

```bash
# This will work (read operation)
curl http://localhost:8000/api/books_all/ \
  -H "Authorization: Token <regular_user_token>"

# This will fail (write operation requires admin)
curl -X POST http://localhost:8000/api/books_all/ \
  -H "Authorization: Token <regular_user_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "author": "Author Name"}'
```

**Expected Response:**
```json
{
    "detail": "You do not have permission to perform this action."
}
```

## Database Migration

After adding `rest_framework.authtoken` to `INSTALLED_APPS`, run migrations:

```bash
python manage.py migrate
```

This creates the `authtoken_token` table needed for token storage.

## Security Best Practices

1. **Never commit tokens to version control**
2. **Use HTTPS in production** to protect tokens in transit
3. **Rotate tokens periodically** for sensitive applications
4. **Store tokens securely** on the client side
5. **Use environment variables** for sensitive configuration

## Troubleshooting

### Token Not Working

1. Verify the token exists: `Token.objects.filter(key='your_token').exists()`
2. Check user is active: `user.is_active`
3. Ensure token is included in Authorization header: `Authorization: Token <token>`

### Permission Denied

1. Check user permissions: `user.is_staff` for admin operations
2. Verify token belongs to the correct user
3. Check the view's permission classes

### Token Endpoint Returns 400

1. Ensure username and password are correct
2. Check request format: `{"username": "...", "password": "..."}`
3. Verify user account is active

## API Endpoints Summary

| Endpoint | Method | Authentication | Permission | Description |
|----------|--------|----------------|------------|-------------|
| `/api/token/` | POST | None | None | Obtain authentication token |
| `/api/books/` | GET | Required | IsAuthenticated | List all books |
| `/api/books_all/` | GET | Required | IsAuthenticated | List all books |
| `/api/books_all/<id>/` | GET | Required | IsAuthenticated | Retrieve a book |
| `/api/books_all/` | POST | Required | IsAdminUser | Create a book |
| `/api/books_all/<id>/` | PUT | Required | IsAdminUser | Update a book |
| `/api/books_all/<id>/` | PATCH | Required | IsAdminUser | Partially update a book |
| `/api/books_all/<id>/` | DELETE | Required | IsAdminUser | Delete a book |

