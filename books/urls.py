from django.urls import path
from books import views
from .views import BookList, BookDetails, BookCreate

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetails.as_view()),
    path('books/create/', views.BookCreate.as_view())
]
