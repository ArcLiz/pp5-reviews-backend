from rest_framework import serializers
from .models import Review
from likes.models import Like


from rest_framework import serializers
from likes.models import Like


class ReviewSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    like_id = serializers.SerializerMethodField()

    def get_owner_name(self, obj):
        return obj.owner.name

    def get_like_id(self, obj):
        try:
            user = self.context['request'].user
            print("User:", user)
            if user.is_authenticated:
                print("User is authenticated")
                like = Like.objects.filter(owner=user, review=obj).first()
                print("Like:", like)
                return like.id if like else None
        except KeyError:
            print("KeyError: 'request' not found in context")
            pass
        return None

    class Meta:
        model = Review
        fields = ['id', 'owner', 'owner_name', 'book',
                  'rating', 'comment', 'created_at', 'updated_at', 'like_id']
