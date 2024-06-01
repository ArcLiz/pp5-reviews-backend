from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ['id', 'owner', 'owner_name', 'book',
                  'rating', 'comment', 'created_at', 'updated_at']

    def get_owner_name(self, obj):
        return obj.owner.name
