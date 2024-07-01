from rest_framework import serializers
from .models import Book, Genre, Series
from reviews.models import Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)
    new_genres = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False)
    series = SeriesSerializer()
    new_series_name = serializers.CharField(write_only=True, required=False)

    def get_reviews_count(self, obj):
        return Review.objects.filter(book=obj).count()

    def create(self, validated_data):
        new_genres = validated_data.pop('new_genres', [])
        new_series_name = validated_data.pop('new_series_name', None)

        genres = validated_data.pop('genres')
        series_data = validated_data.pop('series', None)

        if new_series_name:
            series, created = Series.objects.get_or_create(
                name=new_series_name)
        elif series_data:
            series, created = Series.objects.get_or_create(
                name=series_data['name'])
        else:
            series = None

        book = Book.objects.create(series=series, **validated_data)
        for genre_data in genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'])
            book.genres.add(genre)

        for genre_name in new_genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            book.genres.add(genre)

        return book

    def update(self, instance, validated_data):
        new_genres = validated_data.pop('new_genres', [])
        new_series_name = validated_data.pop('new_series_name', None)

        genres = validated_data.pop('genres', [])
        series_data = validated_data.pop('series', None)

        if new_series_name:
            series, created = Series.objects.get_or_create(
                name=new_series_name)
        elif series_data:
            series, created = Series.objects.get_or_create(
                name=series_data['name'])
        else:
            series = instance.series

        instance.series = series
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.cover_image = validated_data.get(
            'cover_image', instance.cover_image)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        instance.genres.clear()
        for genre_data in genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'])
            instance.genres.add(genre)

        for genre_name in new_genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            instance.genres.add(genre)

        return instance

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_image', 'description',
                  'reviews_count', 'genres', 'new_genres', 'series', 'new_series_name']
