from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_image = models.ImageField(
        upload_to='covers/',
        default='covers/nocover_dhpojf.png',
    )
    description = models.TextField(blank=True)
    genres = models.ManyToManyField(
        'Genre', related_name='books')
    series = models.ForeignKey(
        Series, on_delete=models.SET_NULL, null=True, blank=True)
    series_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
