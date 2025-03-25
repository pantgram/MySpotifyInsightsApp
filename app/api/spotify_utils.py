
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from dotenv import load_dotenv 
load_dotenv

def get_spotify_client_for_user(user):
    """
    Create a Spotify client for a user, refreshing tokens if needed
    
    Args:
        user: User model instance with spotify tokens
        
    Returns:
        spotipy.Spotify instance
    """
    # Check if token is expired
    if user.spotify_token_expires_at  <= timezone.now():
        # Set up OAuth with refresh token
        sp_oauth = SpotifyOAuth(
        )
        
        # Refresh token
        token_info = sp_oauth.refresh_access_token(user.spotify_refresh_token)
        
        # Update user
        user.spotify_access_token = token_info['access_token']
        if 'refresh_token' in token_info:
            user.spotify_refresh_token = token_info['refresh_token']
        
        user.spotify_token_expires_at = timezone.now() + timedelta(seconds=token_info['expires_in'])
        user.save()
    
    # Return Spotify client
    return spotipy.Spotify(auth=user.spotify_access_token)