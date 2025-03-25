from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that adds user info to the token response
    """
    def validate(self, attrs):
        # Call parent validation
        data = super().validate(attrs)
        # Add user data to response
        data['user'] = UserSerializer(self.user).data
        
        return data
