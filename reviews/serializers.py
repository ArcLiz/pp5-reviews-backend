from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import IntegrityError
from .models import Review
from likes.models import Like
from django.db.models import Count
from books.serializers import BookSerializer


class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_avatar = serializers.ReadOnlyField(
        source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    book = BookSerializer(read_only=True)

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.owner == request.user
        return False

    def get_like_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            like = Like.objects.filter(owner=request.user, review=obj).first()
            return like.id if like else None
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['owner'] = request.user
            try:
                return super().create(validated_data)
            except IntegrityError:
                raise serializers.ValidationError(
                    {'detail': 'possible duplicate'})
        raise serializers.ValidationError(
            "You must be logged in to review this book.")

    class Meta:
        model = Review
        fields = ['id', 'owner', 'is_owner', 'like_id', 'likes_count',
                  'book', 'rating', 'comment', 'created_at', 'updated_at', 'owner_avatar']
        extra_kwargs = {'rating': {'validators': [
            MinValueValidator(0), MaxValueValidator(5)]}}
