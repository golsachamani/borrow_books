from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.books, name="books"),
    path("book-detail/<path:author_title>", views.book_detail, name="book-detail"),
    path("book-borrow/<path:author_title>", views.book_borrow, name="book-borrow"),
    path("author-detail/<fullname>", views.author_detail, name="author-detail"),
    path("genre-detail/<name>", views.genre_detail, name="genre-detail"),
]
