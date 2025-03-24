from django.db import models

class TopTracks(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     user_id = models.CharField(max_length=100)
     artist_name = models.CharField(max_length=100)
     track_name = models.CharField(max_length=100)
     track_id = models.CharField(max_length=100)
     uri = models.CharField(max_length=100)
     popularity = models.CharField(max_length=100)
     album_release_date = models.CharField(max_length=100)
