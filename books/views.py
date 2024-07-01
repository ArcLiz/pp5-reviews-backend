from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Book, Genre, Series
from .serializers import BookSerializer, GenreSerializer, SeriesSerializer
from main.permissions import IsAdminOrReadOnly


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


class BookCreate(generics.CreateAPIView):
    """ View to Create a new Book object """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDetails(generics.RetrieveUpdateDestroyAPIView):
    """ Book Details view, **UD for admins """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminOrReadOnly()]


class GenreListCreate(generics.ListCreateAPIView):
    """ Genre List """
    pagination_class = NoPagination
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class GenreDetails(generics.RetrieveUpdateDestroyAPIView):
    """ Genre Details """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class SeriesListCreate(generics.ListCreateAPIView):
    """ Series List """
    pagination_class = NoPagination
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]


class SeriesDetails(generics.RetrieveUpdateDestroyAPIView):
    """ Series Detailing what books are in it """
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
