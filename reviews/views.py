from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Count
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer
from main.permissions import IsAuthorOrReadOnly


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.annotate(
        likes_count=Count('like', distinct=True)
    ).all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner', 'book']


class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.annotate(
        likes_count=Count('like', distinct=True)
    ).all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        self.check_object_permissions(request, review)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
