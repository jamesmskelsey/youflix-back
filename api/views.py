from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, WatchListItemSerializer, GameSerializer, ReviewSerializer, PlayListSerializer
from .models import Review, Game, PlayList, WatchListItem


@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" For reference for later

Shows how to do permission classes and the queryset to filter only objects
belonging to a specific user

class ListViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return List.objects.filter(user_id=user.id)
    serializer_class = ListSerializer
"""


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True)
    def playlists(self, request, pk=None):
        game = self.get_object()
        playlists = game.playlists.all()
        return Response([PlayListSerializer(playlist).data for playlist in playlists])


class WatchListItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return WatchListItem.objects.filter(user=user.id)
    serializer_class = WatchListItemSerializer


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer

    @action(detail=True)
    def reviews(self, request, pk=None):
        playlist = self.get_object()
        reviews = playlist.reviews.all()
        return Response([ReviewSerializer(review).data for review in reviews])


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
