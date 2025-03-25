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
    view_table=[]
    results_table= sp.current_user_top_tracks(limit=20, offset=0, time_range=range)

    for track_info in results_table['items']:
        track_name = track_info['name']
        artists = ', '.join([artist['name'] for artist in track_info['artists']])
        album_release_date = track_info['album']['release_date']
        track_id = track_info['id']
        uri = track_info['uri']
        popularity = track_info['popularity']
        track_data = {
            'artist_name': artists,
            'track_name': track_name,
            'track_id': track_id,
            'uri': uri,
            'popularity': popularity,
            'year': album_release_date
        }
        view_table.append(track_data)
    return Response(view_table)

    



