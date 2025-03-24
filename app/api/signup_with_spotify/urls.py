from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Spotify auth endpoints
    path('spotify/', views.spotify_auth, name='spotify_auth'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    
    # JWT refresh endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]