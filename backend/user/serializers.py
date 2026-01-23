from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    register post req schema
    """
    # each user should have a password
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]
    
    # create user
    def create(self, validated_data):
        return User.objects.create_user(
            name=validated_data['name'], 
            email=validated_data['email'],
            password=validated_data['password']
        )
        
class LoginSerializer(serializers.Serializer):
    """
    login post req schema
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    
    