from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = "relationship_app"

urlpatterns = [
    path("books/", views.list_books, name="book-list"),
    path("add_book/", views.add_book, name="book-add"),
    path("edit_book/<int:pk>/", views.edit_book, name="book-edit"),
    path("delete_book/<int:pk>/", views.delete_book, name="book-delete"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library-detail"),
    # Authentication URLs
    path("login/", LoginView.as_view(template_name="relationship_app/login.html", redirect_authenticated_user=True), name="login"),
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    path("register/", views.register, name="register"),
    # Role-based access control URLs
    path("admin/", views.admin_view, name="admin-view"),
    path("librarian/", views.librarian_view, name="librarian-view"),
    path("member/", views.member_view, name="member-view"),
]

