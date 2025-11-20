from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

app_name = 'api'

# Create a router and register the BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),
    # Token authentication endpoint - allows users to obtain authentication tokens
    # POST /api/token/ with username and password to get a token
    path('token/', obtain_auth_token, name='api-token-auth'),
]

