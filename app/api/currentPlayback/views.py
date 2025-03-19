import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from dotenv import load_dotenv 
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
load_dotenv()
scope = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"




@api_view(['GET'])
def get_recent(request):
    sp = spotipy.Spotify(auth=request.session['token_info']['access_token'])
    results_table= sp.current_user_recently_played(limit=20)
    
    return Response(results_table)

    



