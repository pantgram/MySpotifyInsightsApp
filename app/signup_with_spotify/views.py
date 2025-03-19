import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from dotenv import load_dotenv 
from django.http import HttpResponse,JsonResponse
load_dotenv()
scope = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"



def index(request):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,cache_handler=DjangoSessionCacheHandler(request)))
    return JsonResponse(request.session['token_info'])

    



