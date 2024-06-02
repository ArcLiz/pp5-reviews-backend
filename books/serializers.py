from rest_framework import serializers
from .models import Book
from reviews.models import Review


class BookSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    def get_reviews_count(self, obj):
        return Review.objects.filter(book=obj).count()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_image',
                  'description', 'reviews_count']
