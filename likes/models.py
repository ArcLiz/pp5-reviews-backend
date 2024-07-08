from django.db import models
from django.contrib.auth.models import User
from reviews.models import Review


class Like(models.Model):
    """
    Model for Liking a review
    Allows users to like a review,
    or remove their like to unlike

    attributes:
      owner
      review
      created_at
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'review']

    def __str__(self):
        return f'{self.owner} {self.review}'
