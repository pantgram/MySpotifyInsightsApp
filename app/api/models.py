from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create my user model here
class User(AbstractBaseUser):
    username = models.TextField(unique=True)
    email = models.EmailField(max_length=256, unique=True, verbose_name='email')
    date_of_signup = models.DateTimeField(auto_now_add=True)
    spotify_id = models.TextField()
    is_active = models.BooleanField(default=True)
    spotify_access_token = models.TextField()
    spotify_refresh_token = models.TextField()
    spotify_token_expires_at = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['spotify_access_token', 'spotify_refresh_token', 'spotify_token_expires_at','email']


    def __str__(self):
        return self.username or f"User {self.id}"