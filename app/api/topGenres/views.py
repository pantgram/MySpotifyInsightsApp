from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.spotify_utils import get_spotify_client_for_user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    """
    Fetch the authenticated user's Spotify playlists
    """
    try:
        # Get Spotify client for the authenticated user
        sp = get_spotify_client_for_user(request.user)
        
        # Get playlists
        playlists = sp.current_user_playlists()
        
        return Response(playlists)
    except Exception as e:
        return Response({"error": str(e)}, status=500)