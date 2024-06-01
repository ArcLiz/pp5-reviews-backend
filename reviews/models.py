from django.db import models
from profiles.models import Profile  # Om du använder Profile-modellen
from books.models import Book


class Review(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['owner', 'book']
