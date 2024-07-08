from rest_framework import serializers
from .models import Book
from reviews.models import Review


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    Converts the Book Model instance into JSON format and vice versa

    adding reviews_count to book details
    """
    reviews_count = serializers.SerializerMethodField()

    def get_reviews_count(self, obj):
        return Review.objects.filter(book=obj).count()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_image', 'description',
                  'genres', 'series', 'series_number', 'reviews_count']
