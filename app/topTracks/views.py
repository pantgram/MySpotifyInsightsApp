import spotipy,json
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from dotenv import load_dotenv 
from django.http import HttpResponse,JsonResponse

load_dotenv()
scope = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"



def index(request):
    return HttpResponse("Specify a time range")

def in_time_range(request,range):
    sp = spotipy.Spotify(auth=request.session['token_info']['access_token'])
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
    json_table = json.dumps(view_table)
    return HttpResponse(json_table)

    



