from django.db import models
from django.contrib.postgres.fields import ArrayField


class Book(models.Model):
    """
    Represents a book in the library

    Attributes:
      title, author, cover_image, description,
      genres, series, series_number
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_image = models.ImageField(
        upload_to='covers/',
        default='covers/nocover_dhpojf.png',
    )
    description = models.TextField(blank=True)
    genres = ArrayField(models.CharField(
        max_length=100), blank=True, default=list)
    series = models.CharField(max_length=200, null=True, blank=True)
    series_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
