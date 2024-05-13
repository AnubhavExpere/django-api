from rest_framework.routers import DefaultRouter
from . import views 
from django.urls import path

router = DefaultRouter()
router.register(r'songs', views.SongsViewSet, basename='songs')
router.register(r'playlists', views.PlaylistViewSet, basename='playlists')
router.register(r'playlists/(?P<playlist_id>[^/.]+)/songs', views.PlaylistSongViewSet, basename='songs-in-playlist')
urlpatterns = router.urls


# urlpatterns = [
#     path('songs/', views.ListSongsView.as_view(), name='list-songs'),
# ]