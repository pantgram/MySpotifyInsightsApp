import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from dotenv import load_dotenv 
from rest_framework.decorators import api_view
from rest_framework.response import Response
load_dotenv()
scope = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"




@api_view(['GET'])
def get_recent(request):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,cache_handler=DjangoSessionCacheHandler(request)))
    results_table= sp.current_user_recently_played(limit=20)
    view_table=[]
    for playback_info in results_table['items']:
        track_info = playback_info['track']
        album_info = track_info['album']
        track_name = track_info['name']
        artists = ', '.join([artist['name'] for artist in track_info['artists']])
        album_release_date = track_info['album']['release_date']
        track_id = track_info['id']
        uri = track_info['uri']
        popularity = track_info['popularity']
        played_at = playback_info['played_at']
        album_name = album_info['name']
        playback_data = {
            'artist_name': artists,
            'album_name': album_name,
            'track_name': track_name,
            'track_id': track_id,
            'uri': uri,
            'popularity': popularity,
            'year': album_release_date,
            'played_at':played_at
        }
        view_table.append(playback_data)
    return Response(view_table)

    



