import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from dotenv import load_dotenv 
from django.http import HttpResponse,JsonResponse
load_dotenv()
scope = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

def spotify_auth(request):
    # Create cache handler using Django session

    
    # Create SpotifyOAuth with session cache handler
    sp_oauth = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,cache_handler=DjangoSessionCacheHandler(request)))
    
    # Get the authorization URL
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    # Create cache handler using Django session

    
    # Create SpotifyOAuth with session cache handler
    sp_oauth =spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,cache_handler=DjangoSessionCacheHandler(request)))
    
    # Get auth code from request
    code = request.GET.get("code")
    
    # Exchange code for token info (this will also cache tokens in session)
    token_info = sp_oauth.get_access_token(code)
    
    # Create Spotify client using the OAuth manager which already has tokens
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    
    # Get user profile
    profile_data = sp.current_user()
    
    # Get or create user
    user, created = User.objects.get_or_create(
        spotify_id=profile_data["id"],
        defaults={
            "username": profile_data.get("display_name", f"spotify_{profile_data['id']}"),
            "email": profile_data.get("email", ""),
        }
    )
    
    # Set unusable password for new users
    if created:
        user.set_unusable_password()
        user.save()
    
    # Create your own JWT token
    refresh = RefreshToken.for_user(user)
    
    # Save the Spotify user ID in the session
    request.session['spotify_user_id'] = profile_data["id"]
    
    # Return tokens to frontend
    return JsonResponse({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })

    



