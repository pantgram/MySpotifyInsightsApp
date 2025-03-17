import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from dotenv import load_dotenv 
from django.http import HttpResponse
load_dotenv()
scope = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"



def index(request):
    return HttpResponse("Specify a time range")

def in_time_range(request,range):
    sp = spotipy.Spotify(auth=request.session['token_info']['access_token'])
    results_table= sp.current_user_top_artists(limit=20, offset=0, time_range=range)
    for row in results_table:
        track = row
    print(request.session['token_info'])
    return HttpResponse(track)

    



