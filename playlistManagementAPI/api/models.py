from django.db import models

class Song(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()

    def __int__(self):
        return self.id

class PlaylistSong(models.Model):
    playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, through='PlaylistSong' ,related_name='song')

    def __str__(self):
        return self.name