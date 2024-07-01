from rest_framework import serializers
from .models import Book, Genre, Series
from reviews.models import Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class SeriesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Series
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ['id', 'owner', 'rating',
                  'comment', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)
    series = SeriesSerializer(required=False)
    reviews_count = serializers.SerializerMethodField()

    def get_reviews_count(self, obj):
        return Review.objects.filter(book=obj).count()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_image', 'description',
                  'genres', 'series', 'series_number', 'reviews_count']

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        series_data = validated_data.pop('series', None)
        book = Book.objects.create(**validated_data)

        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'])
            book.genres.add(genre)

        if series_data and series_data.get('name'):
            series, created = Series.objects.get_or_create(
                name=series_data['name'])
            book.series = series

        book.save()
        return book

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        series_data = validated_data.pop('series', None)

        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.cover_image = validated_data.get(
            'cover_image', instance.cover_image)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.series_number = validated_data.get(
            'series_number', instance.series_number)

        if genres_data is not None:
            instance.genres.clear()
            for genre_data in genres_data:
                genre, created = Genre.objects.get_or_create(
                    name=genre_data['name'])
                instance.genres.add(genre)

        if series_data is not None:
            if series_data.get('name'):
                series, created = Series.objects.get_or_create(
                    name=series_data['name'])
                instance.series = series
            else:
                instance.series = None

        instance.save()
        return instance
