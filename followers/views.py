from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from main.permissions import IsOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    """
    List all followers, i.e. all instances of a user
    following another user'.
    Create a follower, i.e. follow a user if logged in.
    Perform_create: associate the current logged in user with a follower.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower
    No Update view, as we either follow or unfollow users
    Destroy a follower, i.e. unfollow someone if owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer


@api_view(['POST', 'DELETE'])
def follow_user(request, followed_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Unauthorized'},
                        status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'POST':
        # Check if user already follows the specified user
        existing_followers = Follower.objects.filter(
            owner=request.user, followed=followed_id)
        if existing_followers.exists():
            return Response({'error': 'User already followed'},
                            status=status.HTTP_200_OK)

        # Create a new follower instance
        follower_data = {'owner': request.user.id, 'followed': followed_id}
        serializer = FollowerSerializer(data=follower_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Check if the follower exists
        try:
            follower_to_delete = Follower.objects.get(
                owner=request.user, followed=followed_id)
        except Follower.DoesNotExist:
            return Response({'error': 'Follower does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        # Remove the follow
        follower_to_delete.delete()
        return Response({'message': 'Unfollowed user'},
                        status=status.HTTP_200_OK)
