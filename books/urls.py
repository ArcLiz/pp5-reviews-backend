from django.urls import path
from .views import BookList, BookDetails, BookCreate, GenreListCreate, SeriesListCreate, SeriesDetails

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetails.as_view(), name='book-details'),
    path('books/create/', BookCreate.as_view(), name='book-create'),
    path('genres/', GenreListCreate.as_view(), name='genre-list-create'),
    path('series/', SeriesListCreate.as_view(), name='series-list-create'),
    path('series/<int:pk>/', SeriesDetails.as_view(), name='series-list-create'),
]
