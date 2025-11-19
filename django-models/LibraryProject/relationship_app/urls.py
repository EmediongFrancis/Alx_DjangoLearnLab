from django.urls import path

from .views import CustomLoginView
from .views import CustomLogoutView
from .views import LibraryDetailView
from .views import list_books
from .views import register

app_name = "relationship_app"

urlpatterns = [
    path("books/", list_books, name="book-list"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),
    # Authentication URLs
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
]

