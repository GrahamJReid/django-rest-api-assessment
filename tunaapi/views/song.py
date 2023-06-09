"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song, SongGenre



class SongView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song, context={'request': request})
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
          
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        artist = Artist.objects.get(pk=request.data["artist_id"])
        
        song = Song.objects.create(
            title=request.data["title"],
            artist_id=artist,
            album=request.data["album"],
            length=request.data["length"],
            
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)
      
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        artist = Artist.objects.get(pk=request.data["artist_id"])
        
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.artist_id = artist
        song.album = request.data["album"]
        song.length = request.data["length"]
      
        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
    def destroy(self, request, pk):
        """Delete Artists
        """
        artist = Song.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)   
      

class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    class Meta:
        model = SongGenre
        fields = ( 'genre_id',)     
        depth = 1
            
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""

    artist = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length', 'genres')
        
    def get_genres(self, obj):
      genres = obj.genres.all()
      return [{'id': genre.genre_id.id, 'description': genre.genre_id.description} for genre in genres]
    def get_artist(self, obj):
      artist = obj.artist_id
      return [{'id': artist.id, 'name': artist.name,'age': artist.age, 'bio': artist.bio}]
