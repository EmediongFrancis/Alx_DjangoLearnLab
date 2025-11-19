from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = "relationship_app"

urlpatterns = [
    path("books/", views.list_books, name="book-list"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library-detail"),
    # Authentication URLs
    path(
        "login/",
        LoginView.as_view(
            template_name="relationship_app/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    path("register/", views.register, name="register"),
]

