from rest_framework import serializers
from .models import Book
from reviews.models import Review


class BookSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    def get_reviews_count(self, obj):
        return Review.objects.filter(book=obj).count()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_image', 'description',
                  'genres', 'series', 'series_number', 'reviews_count']

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.cover_image = validated_data.get(
            'cover_image', instance.cover_image)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.genres = validated_data.get('genres', instance.genres)
        instance.series = validated_data.get('series', instance.series)
        instance.series_number = validated_data.get(
            'series_number', instance.series_number)

        instance.save()
        return instance
