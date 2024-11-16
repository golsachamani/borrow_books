from django.contrib import admin
from . import models


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname")


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "get_genres", "pages")

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("id", "instance_of", "status", "borrower")


admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookInstace, BookInstanceAdmin)
