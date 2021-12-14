from django.urls import path
from .views import current_user, UserList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'lists', ListViewSet, basename="lists")
#router.register(r'tasks', TaskViewSet, basename="tasks")

urlpatterns = router.urls

urlpatterns += [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
]
