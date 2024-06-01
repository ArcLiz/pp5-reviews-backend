from django.urls import path
from .views import ReviewList, ReviewDetail, ProfileReviews, BookReviews

urlpatterns = [
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('profiles/<int:owner_id>/reviews/',
         ProfileReviews.as_view(), name='profile-reviews'),
    path('books/<int:pk>/reviews/',
         BookReviews.as_view(), name='book-reviews'),
]
