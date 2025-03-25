import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from django.utils import timezone
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import  timedelta
from dotenv import load_dotenv 
load_dotenv()

from api.models import User
from api.serializers import UserSerializer

class SpotifyAuthView(views.APIView):
    """
    Handle Spotify authentication and user creation/update
    """
    permission_classes = [AllowAny]
    scope_auth = "user-library-read playlist-read-private user-library-modify user-read-recently-played user-top-read playlist-modify-public playlist-modify-private app-remote-control user-modify-playback-state"

    
    def get(self, request):
        """
        Get Spotify authorization URL
        """
        sp_oauth = SpotifyOAuth(scope=self.scope_auth)
        try:
            token_info = sp_oauth.get_access_token()

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user profile
        sp = spotipy.Spotify(auth=token_info['access_token'])
        try:
            profile = sp.me()
        except Exception as e:
            return Response({"error": f"Failed to get Spotify profile: {str(e)}"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate token expiry time
        expires_at = timezone.now() + timedelta(seconds=token_info['expires_in'])
        
        # Create or update user
        try:
            user, created = User.objects.update_or_create(
                spotify_id=profile['id'],
                defaults={
                    'username': profile.get('display_name') or profile['id'],
                    'email': profile.get('email', ''),
                    'spotify_access_token': token_info['access_token'],
                    'spotify_refresh_token': token_info.get('refresh_token'),
                    'spotify_token_expires_at': expires_at
                }
            )
            
            if created:
                user.set_unusable_password()
                user.save()
                
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            
        except Exception as e:
            return Response({"error": f"User creation failed: {str(e)}"}, 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileView(views.APIView):
    """
    View for retrieving and updating the authenticated user's profile
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get the current user's profile
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)