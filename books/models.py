from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Enter a book genre (e.g 'sci-fi')",
    )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="genre_name_lower_unique_constrain",
                violation_error_message="Duplicate genre name (NOTE: genre name is case-insensitive)",
            )
        ]

    def get_absolute_url(self):
        return reverse("genre-detail", args=[f"{self.name}"])


class Author(models.Model):
    fullname = models.CharField(max_length=127, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to='authors.image', null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("fullname"),
                name="author_fullname_lower_unique_constrain",
                violation_error_message="Duplicate author name (NOTE: author name is case-insensitive)",
            )
        ]

    def __str__(self) -> str:
        return self.fullname

    def get_absolute_url(self):
        return reverse("author-detail", args=[f"{self.fullname}"])


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    pages = models.PositiveIntegerField()
    genre = models.ManyToManyField(Genre, related_name="book")
    published_at = models.DateTimeField()
    img = models.ImageField(upload_to='books.image', null=True)
    short_desc = models.TextField(max_length=1023, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("book-detail", args=[f"{self.author.fullname}/{self.title}"])

    def get_borrow_url(self):
        return reverse("book-borrow", args=[f"{self.author.fullname}/{self.title}"])

    def get_genres(self):
        return [genre.name for genre in self.genre.all()]
    get_genres.short_description = "genres"

    @property
    def instances(self):
        return BookInstace.objects.filter(book__exact=self.id)

    @property
    def available_instances(self):
        return [
            v for v in self.instances.all() if v.status == BookInstaceStatus.Available
        ]
        # return self.instances.filter(status__exact=BookInstaceStatus.Available)

    def borrow(self, user: User, due_time: datetime):
        availables = self.available_instances
        if len(availables) < 1:
            raise Exception(f"{str(self)} has no available instance to borrow")

        availables[0].borrow(user, due_time)


class BookInstaceStatus:
    Available = "available"
    Borrowed = "borrowed"
    Maintainance = "maintainance"


class BookInstace(models.Model):
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    borrower = models.ForeignKey(
        User, on_delete=models.RESTRICT, null=True, blank=True)
    borrow_due_time = models.DateField(null=True, blank=True)
    maintain_due_time = models.DateField(null=True, blank=True)

    @property
    def status(self):
        if self.borrower or self.borrow_due_time:
            return BookInstaceStatus.Borrowed

        if self.maintain_due_time:
            return BookInstaceStatus.Maintainance

        return BookInstaceStatus.Available

    @property
    def is_availabe(self):
        return self.status == BookInstaceStatus.Available

    def instance_of(self):
        return f"{self.book.title} by {self.book.author.fullname}"

    def get_absolute_url(self):
        return reverse("book-instance", args=[f"{self.id}"])

    def borrow(self, borrower: User, due_time: datetime):
        if not self.is_availabe:
            raise Exception(f"{BookInstace.id} is not available")

        self.borrower = borrower
        self.borrow_due_time = due_time
        self.save()
