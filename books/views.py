from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from . import models
from datetime import datetime, timedelta


def home(request):
    books = models.Book.objects.all()
    context = {
        "title": "Welcome",
        "books": books,
        
    }
    return render(request=request, template_name="home.html", context=context)


def books(request):
    books = models.Book.objects.all()
    context = {
        "title": "Books",
        "books": books,
    }
    return render(request=request, template_name="books.html", context=context)


def book_detail(request, author_title):
    author, title = author_title.split("/")
    book = models.Book.objects.filter(
        title__iexact=title, author__fullname__iexact=author
    ).get()
    context = {
        "title": book.title,
        "book": book,
    }
    return render(request=request, template_name="book-detail.html", context=context)


def book_borrow(request: HttpRequest, author_title):
    author, title = author_title.split("/")
    book = models.Book.objects.filter(
        title__iexact=title, author__fullname__iexact=author
    ).get()

    due_time = datetime.now() + timedelta(days=10)
    user = request.user
    book.borrow(user, due_time)

    return redirect(reverse("book-detail", args=[author_title]))


def book_instance(request, id):
    book_instance = models.BookInstace.objects.get(pk=id)
    context = {
        "title": book_instance.book.title,
        "book_instance": book_instance,
    }
    return render(request=request, template_name="book-instance.html", context=context)


def author_detail(request, fullname):
    author = models.Author.objects.filter(fullname__iexact=fullname).get()
    context = {
        "title": author.fullname,
        "author": author,
    }
    return render(request, template_name="author-detail.html", context=context)


def genre_detail(request, name):
    genre = models.Genre.objects.filter(name__iexact=name).get()
    context = {
        "title": f"genre {genre.name}",
        "genre": genre,
    }
    return render(request, template_name="genre-detail.html", context=context)
