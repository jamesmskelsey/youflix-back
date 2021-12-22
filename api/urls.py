from django.urls import path
from .views import GameViewSet, PlayListViewSet, ReviewViewSet, WatchListItemViewSet, current_user, UserList, current_access_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='games')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'playlists', PlayListViewSet, basename='playlists')
router.register(r'watchlists', WatchListItemViewSet, basename='watchlists')

urlpatterns = router.urls

urlpatterns += [
    path('current_access_token/', current_access_token),
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
]
