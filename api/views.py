from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, WatchListItemSerializer, GameSerializer, ReviewSerializer, PlayListSerializer
from .models import Review, Game, PlayList, WatchListItem


@api_view(['GET'])
def current_access_token(request):
    return Response({
        "client_id": "enlqcn8re8huq4yqzi6j5hchi022av",
        "access_token": "idicjq3p7bogyuh97aea5a2h9mfgs3"
    })

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
        print(user)
        return WatchListItem.objects.filter(user=user.id)

    def create(self, request):
        user = self.request.user
        print(f"Creating watchlist item for user: {user}, {request.data}")
        item = user.watchlist.create(playlist_id=request.data['playlist_id'])
        return Response(WatchListItemSerializer(item).data)
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

    def create(self, request):
        user = self.request.user
        print(f"creating review for user: {user} {request.data}")
        review = user.reviews.create(
            user=user,
            playlist_id=request.data['playlist_id'],
            rating=request.data['rating'],
            review_text=request.data['review_text']
        )
        return Response(ReviewSerializer(review).data)

    def partial_update(self, request, pk=None):
        user = self.request.user
        review = get_object_or_404(Review, pk=pk)
        print(f"updating review for user {user} {request.data} {review}")
        if user == review.user:
            Review.objects.filter(id=pk).update(**request.data)
            review.refresh_from_db()
        return Response(ReviewSerializer(review).data)

    serializer_class = ReviewSerializer
