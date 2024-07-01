from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Book, Genre, Series
from .serializers import BookSerializer, GenreSerializer, SeriesSerializer
from main.permissions import IsAdminOrReadOnly
from django.http import Http404


class BookList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetails(APIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        try:
            book = self.get_object(pk)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookCreate(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        genres_data = self.request.data.pop('genres', [])
        new_genres_data = self.request.data.pop('new_genres', [])

        series_data = self.request.data.pop('series', None)
        new_series_name = self.request.data.pop('new_series_name', None)

        if new_series_name:
            series, created = Series.objects.get_or_create(
                name=new_series_name)
        elif series_data:
            series, created = Series.objects.get_or_create(**series_data)
        else:
            series = None

        book = serializer.save(series=series, **self.request.data)

        for genre_id in genres_data:
            genre = Genre.objects.get(id=genre_id)
            book.genres.add(genre)

        for genre_name in new_genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            book.genres.add(genre)

        return book


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAdminOrReadOnly]


class SeriesListCreate(generics.ListCreateAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAdminOrReadOnly]


class SeriesDetails(APIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            series = Series.objects.get(pk=pk)
        except Series.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        books = Book.objects.filter(series=series)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
