# reviews/views.py
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Review
from books.models import Book
from .serializers import ReviewSerializer
from main.permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly


from django.db.models import Count


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.annotate(likes_count=Count('like')).all()
    serializer_class = ReviewSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'book__title'
    ]
    ordering_fields = [
        'likes_count'
    ]


class ReviewDetail(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        review = self.get_object(pk)
        review_with_likes_count = Review.objects.annotate(
            likes_count=Count('like')).get(pk=pk)
        serializer = ReviewSerializer(
            review_with_likes_count, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileReviews(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = ReviewSerializer

    def get(self, request, owner_id):
        reviews = Review.objects.filter(owner_id=owner_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class BookReviews(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = ReviewSerializer

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            reviews = Review.objects.filter(book=book)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(status=404)


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)