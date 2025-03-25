from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv 
from rest_framework.response import Response
from api.spotify_utils import get_spotify_client_for_user
load_dotenv()
scope = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    return Response("Specify a time range")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def in_time_range(request,range):
    sp = get_spotify_client_for_user(request.user)
    results_table= sp.current_user_top_artists(limit=20, offset=0, time_range=range)
    view_table = []
    for artist_info in results_table['items']:
        artist_name = artist_info['name']
        artist_genres = artist_info['genres']
        artist_id = artist_info['id']
        uri = artist_info['uri']
        popularity = artist_info['popularity']
        artist_data = {
            'artists_name': artist_name,
            'artist_id': artist_id,
            'uri': uri,
            'genres': artist_genres,
            'popularity': popularity,
        }
        view_table.append(artist_data)
    return Response(view_table)

    



