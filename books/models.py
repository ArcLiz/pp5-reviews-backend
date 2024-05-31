from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='covers/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title