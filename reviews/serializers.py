from rest_framework import serializers
from django.db import IntegrityError
from .models import Review
from likes.models import Like
from django.db.models import Count


class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, review=obj
            ).first()
            return like.id if like else None
        return None

    def get_likes_count(self, obj):
        return obj.likes_count

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['owner'] = request.user
            try:
                return super().create(validated_data)
            except IntegrityError:
                raise serializers.ValidationError({
                    'detail': 'possible duplicate'
                })
        raise serializers.ValidationError(
            "You must be logged in to review this book.")

    class Meta:
        model = Review
        fields = ['id', 'owner', 'is_owner', 'book',
                  'rating', 'comment', 'created_at', 'updated_at', 'like_id', 'likes_count']
