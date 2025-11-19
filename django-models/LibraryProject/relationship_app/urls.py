from django.urls import path

from .views import LibraryDetailView, book_list_view

app_name = "relationship_app"

urlpatterns = [
    path("books/", book_list_view, name="book-list"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),
]

