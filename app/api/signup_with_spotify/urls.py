from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SpotifyAuthView, UserProfileView

urlpatterns = [
    # Spotify auth endpoint
    path('auth/spotify/', SpotifyAuthView.as_view(), name='spotify_auth'),
    
    # JWT refresh endpoint
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoint
    path('users/me/', UserProfileView.as_view(), name='user_profile'),
]
