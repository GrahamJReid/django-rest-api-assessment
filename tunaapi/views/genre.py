"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre



class GenreView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
          
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        genre = Genre.objects.all()
        serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        
        genre = Genre.objects.create(
            description=request.data["description"],
            
            
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
      
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        
      
        genre.save()

        return Response(None, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        """Delete Artists
        """
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT) 
      
class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres"""

    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    artist_id = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    length = serializers.SerializerMethodField()

    class Meta:
        model = SongGenre
        fields = ('id', 'title', 'artist_id', 'album', 'length')

    def get_id(self, obj):
        return obj.song_id.id

    def get_title(self, obj):
        return obj.song_id.title

    def get_artist_id(self, obj):
        return obj.song_id.artist_id.id

    def get_album(self, obj):
        return obj.song_id.album

    def get_length(self, obj):
        return obj.song_id.length   
                  
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    songs = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        depth = 1
    
