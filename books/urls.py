from django.urls import path
from .views import BookList, BookDetails, BookCreate

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetails.as_view(), name='book-details'),
    path('books/create/', BookCreate.as_view(), name='book-create'),
]
