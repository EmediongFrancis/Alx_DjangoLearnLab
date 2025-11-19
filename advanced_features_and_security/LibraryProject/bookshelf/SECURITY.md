# Security Implementation Guide

This document details the security measures implemented in the Django bookshelf application to protect against common web vulnerabilities.

## Table of Contents

1. [Security Settings](#security-settings)
2. [CSRF Protection](#csrf-protection)
3. [SQL Injection Prevention](#sql-injection-prevention)
4. [XSS Protection](#xss-protection)
5. [Content Security Policy](#content-security-policy)
6. [Input Validation](#input-validation)
7. [Testing Security](#testing-security)

## Security Settings

### Configuration in `settings.py`

The application includes comprehensive security settings:

#### Browser Security Headers

```python
# XSS Protection
SECURE_BROWSER_XSS_FILTER = True  # Enables browser's XSS filter

# Content Type Protection
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents MIME type sniffing

# Frame Options
X_FRAME_OPTIONS = 'DENY'  # Prevents clickjacking attacks
```

#### Cookie Security

```python
# CSRF Cookie Settings
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevents JavaScript access

# Session Cookie Settings
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access
```

**Important**: In production with HTTPS, set `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` to `True`.

#### Debug Mode

```python
# Always set DEBUG to False in production
DEBUG = True  # Development only!
```

**Warning**: Never deploy with `DEBUG = True` in production. It exposes sensitive information.

## CSRF Protection

### Implementation

All forms in the application include CSRF tokens to prevent Cross-Site Request Forgery (CSRF) attacks.

#### In Templates

```django
<form method="post">
    {% csrf_token %}  <!-- Required for all POST forms -->
    <!-- form fields -->
</form>
```

#### How It Works

1. Django generates a unique CSRF token for each user session
2. The token is included in forms via `{% csrf_token %}`
3. On form submission, Django validates the token
4. Invalid or missing tokens result in a 403 Forbidden error

#### CSRF Middleware

The `CsrfViewMiddleware` is enabled in `settings.py`:

```python
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    # ...
]
```

## SQL Injection Prevention

### Using Django ORM

**Never use raw SQL queries with string formatting!**

#### ❌ Insecure (Vulnerable to SQL Injection)

```python
# DON'T DO THIS!
query = f"SELECT * FROM books WHERE title = '{user_input}'"
Book.objects.raw(query)
```

#### ✅ Secure (Using Django ORM)

```python
# Django ORM automatically parameterizes queries
books = Book.objects.filter(title__icontains=user_input)
```

### Implementation in Views

All database queries use Django's ORM, which automatically:

1. **Parameterizes queries**: User input is never directly inserted into SQL
2. **Escapes special characters**: Prevents SQL injection attacks
3. **Validates data types**: Ensures type safety

#### Example: Secure Search

```python
# In views.py
from django.db.models import Q

def book_list(request):
    query = request.GET.get('query', '')
    # Using Q objects for safe query construction
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )
    # Django ORM automatically parameterizes this query
```

## XSS Protection

### Template Auto-Escaping

Django templates automatically escape output to prevent XSS attacks.

#### Automatic Escaping

```django
<!-- This is automatically escaped -->
<p>{{ user_input }}</p>

<!-- Explicit escaping (redundant but clear) -->
<p>{{ user_input|escape }}</p>
```

#### Manual Escaping (When Needed)

If you need to output HTML, use the `safe` filter carefully:

```django
<!-- Only use if you're certain the content is safe -->
<p>{{ trusted_html|safe }}</p>
```

### Input Sanitization

All user input is validated and sanitized through Django forms:

```python
# In forms.py
class BookForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Strip whitespace and validate
        title = title.strip()
        if len(title) < 2:
            raise ValidationError('Title too short')
        return title
```

## Content Security Policy

### Implementation

A custom CSP middleware adds Content Security Policy headers to all responses.

#### Middleware Location

`bookshelf/middleware.py`

#### CSP Policy

```python
csp_policy = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none';"
)
```

#### How CSP Works

1. Browser receives CSP header with policy
2. Browser only loads resources from allowed sources
3. Violations are blocked and reported
4. Prevents XSS attacks by restricting script execution

## Input Validation

### Django Forms

All user input is validated using Django forms:

#### Form Definition

```python
# In forms.py
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        # Custom validation
        title = self.cleaned_data.get('title')
        title = title.strip()  # Sanitize
        if len(title) < 2:
            raise ValidationError('Title too short')
        return title
```

#### Form Usage in Views

```python
# In views.py
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # All input is validated and sanitized
            book = form.save()
            return redirect('bookshelf:book-detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})
```

### Validation Benefits

1. **Type checking**: Ensures correct data types
2. **Length validation**: Prevents buffer overflows
3. **Format validation**: Ensures data format is correct
4. **Sanitization**: Removes dangerous characters

## Testing Security

### Manual Testing Checklist

#### CSRF Protection

1. ✅ All forms include `{% csrf_token %}`
2. ✅ POST requests without CSRF token are rejected
3. ✅ CSRF token is validated on form submission

#### SQL Injection

1. ✅ All queries use Django ORM (no raw SQL)
2. ✅ User input is never directly inserted into queries
3. ✅ Search functionality uses parameterized queries

#### XSS Protection

1. ✅ Template output is automatically escaped
2. ✅ User input is sanitized in forms
3. ✅ No unsafe HTML rendering

#### Input Validation

1. ✅ Forms validate all required fields
2. ✅ Invalid input is rejected with error messages
3. ✅ Data types are validated

### Testing Commands

#### Test CSRF Protection

```bash
# Try to submit a form without CSRF token
curl -X POST http://localhost:8000/books/create/ \
  -d "title=Test&author=Author&publication_year=2024"
# Should return 403 Forbidden
```

#### Test SQL Injection

```bash
# Try SQL injection in search
curl "http://localhost:8000/books/?query=' OR '1'='1"
# Should not execute SQL, just return empty results
```

#### Test XSS Protection

```bash
# Try XSS in form
curl -X POST http://localhost:8000/books/create/ \
  -H "Cookie: csrftoken=..." \
  -d "title=<script>alert('XSS')</script>&author=Author&publication_year=2024"
# Script tags should be escaped in output
```

## Production Checklist

Before deploying to production:

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set `CSRF_COOKIE_SECURE = True` (requires HTTPS)
- [ ] Set `SESSION_COOKIE_SECURE = True` (requires HTTPS)
- [ ] Enable HTTPS/SSL
- [ ] Configure proper CSP policy for your CDN/external resources
- [ ] Review and test all security settings
- [ ] Keep Django and dependencies updated
- [ ] Use environment variables for sensitive settings (SECRET_KEY)

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Content Security Policy Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

## Security Best Practices Summary

1. **Always use Django forms** for user input
2. **Never use raw SQL** with string formatting
3. **Always include CSRF tokens** in forms
4. **Let Django templates escape** output automatically
5. **Validate and sanitize** all user input
6. **Use HTTPS in production** and set secure cookie flags
7. **Keep Django updated** to latest security patches
8. **Review security settings** before deployment

