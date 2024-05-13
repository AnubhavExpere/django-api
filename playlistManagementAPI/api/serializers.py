from rest_framework import serializers
from .models import Song, Playlist, PlaylistSong

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name']


class PlaylistSongSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='song.id')
    name = serializers.CharField(source='song.name')
    artist = serializers.CharField(source='song.artist')
    release_year = serializers.IntegerField(source='song.release_year')

    class Meta:
        model = PlaylistSong
        fields = ['id', 'name', 'artist', 'release_year', 'position']

class PaginatedSongSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = SongSerializer(many=True)

