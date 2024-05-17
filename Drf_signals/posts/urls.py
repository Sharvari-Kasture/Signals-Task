from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, BlockedUserListCreateAPIView, BlockedUserRetrieveDestroyAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
    path('blocked-users/', BlockedUserListCreateAPIView.as_view(), name='blocked-user-list-create'),
    path('blocked-users/<int:pk>/', BlockedUserRetrieveDestroyAPIView.as_view(), name='blocked-user-retrieve-destroy'),
]