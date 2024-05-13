from .models import Song, Playlist, PlaylistSong
from .serializers import SongSerializer, PlaylistSerializer, PlaylistSongSerializer, PaginatedSongSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class MyPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class SongsViewSet(ModelViewSet):
    queryset = Song.objects.order_by('id')
    serializer_class = SongSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = Song.objects.all()
        name = self.request.query_params.get('q')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    def create(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.order_by('id')
    serializer_class = PlaylistSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = Playlist.objects.all()
        name = self.request.query_params.get('q')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    def create(self, request):
        name = request.data.get('name')
        song_ids = request.data.get('songs')
        playlist = Playlist.objects.create(name=name)
        for position, song_id in enumerate(song_ids, start=1):
            try:
                song = Song.objects.get(pk=song_id)
            except Song.DoesNotExist:
                return Response({"error": f"Song with id {song_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            PlaylistSong.objects.create(playlist=playlist, song=song, position=position)

        serializer = PlaylistSerializer(playlist)
        return Response(status=status.HTTP_201_CREATED)    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)
    
class PlaylistSongViewSet(ModelViewSet):
    queryset = PlaylistSong.objects.all()
    pagination_class = MyPagination
    serializer_class = PlaylistSongSerializer

    def list(self, request, *args, **kwargs):
        playlist_id = self.kwargs['playlist_id']
        queryset = self.filter_queryset(self.get_queryset().filter(playlist_id=playlist_id))
        queryset = queryset.order_by('position')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        playlist_id = kwargs.get('playlist_id')
        song_id = kwargs.get('pk')
        song_ids = Playlist.objects.get(pk=playlist_id).songs.all().values_list('id', flat=True)
        new_position = request.data.get('position')

        if new_position < 1 or new_position > PlaylistSong.objects.filter(playlist_id=playlist_id).count():
            return Response({"error": "Invalid position."}, status=status.HTTP_400_BAD_REQUEST)

        songs_id_list = []
        for i in song_ids:
            songs_id_list.append(i)
        songs_id_list.remove(int(song_id))
        songs_id_list.insert(new_position - 1, song_id)

        for position, song_id in enumerate(songs_id_list, start=1):
            try:
                playlist_song = PlaylistSong.objects.get(playlist_id=playlist_id, song_id=song_id)
            except PlaylistSong.DoesNotExist:
                return Response({"error": f"Song with id {song_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            playlist_song.position = position
            playlist_song.save()

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        print("destroy")
        playlist_id = kwargs.get('playlist_id')
        song_id = kwargs.get('pk')
        song_ids = Playlist.objects.get(pk=playlist_id).songs.all().values_list('id', flat=True)

        songs_id_list = []
        for i in song_ids:
            songs_id_list.append(i)

        if int(song_id) not in songs_id_list: 
            return Response({"error": "Song not found in the playlist."}, status=status.HTTP_404_NOT_FOUND)

        playlist_song_del = PlaylistSong.objects.get(playlist_id=playlist_id, song_id=song_id)
        playlist_song_del.delete()
        songs_id_list.remove(int(song_id))

        for position, song_id in enumerate(songs_id_list, start=1):
            try:
                playlist_song = PlaylistSong.objects.get(playlist_id=playlist_id, song_id=song_id)
            except PlaylistSong.DoesNotExist:
                return Response({"error": f"Song with id {song_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            playlist_song.position = position
            playlist_song.save()
        return Response(status=status.HTTP_200_OK)