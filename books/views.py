from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Book, Genre, Series
from .serializers import BookSerializer, GenreSerializer, SeriesSerializer
from main.permissions import IsAdminOrReadOnly
from django.http import Http404


class NoPagination(PageNumberPagination):
    """ To remove global pagination on genre and series classes """
    page_size = None


class BookList(APIView):
    """ View of all books """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetails(APIView):
    """ View of book:id details """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]

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
    permission_classes = [IsAuthenticated]

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
    pagination_class = NoPagination
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class GenreDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class SeriesListCreate(generics.ListCreateAPIView):
    pagination_class = NoPagination
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]


class SeriesDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        books = Book.objects.filter(series=instance)
        books_serializer = BookSerializer(books, many=True)

        response_data = {
            'series': serializer.data,
            'books': books_serializer.data,
        }

        return Response(response_data)
