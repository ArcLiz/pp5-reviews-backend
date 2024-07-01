from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'series', 'series_number')
    list_filter = ('genres', 'series')
    search_fields = ('title', 'author')
