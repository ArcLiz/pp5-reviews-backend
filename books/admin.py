from django.contrib import admin
from .models import Book, Genre, Series


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'series', 'series_number')
    list_filter = ('genres', 'series')
    search_fields = ('title', 'author')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
