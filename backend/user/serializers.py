from rest_framework import serializers
from .models import User
from bookings.models import Booking

from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT=MongoClient(os.getenv("MONGO_URI"))
DATABASE=CLIENT[os.getenv("MONGO_DB_NAME")]

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
    
    
class UserBooked(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class Activity(serializers.ModelSerializer):
    user_name = serializers.CharField(source="name")
    user_email = serializers.CharField(source="email")
    bookings = serializers.SerializerMethodField()
    searches = serializers.SerializerMethodField()
    
    def get_bookings(self, user):
        all_bookings = Booking.objects.filter(user=user).select_related("train")
        
        return [
            {
                "Train": booking.train.name,
                "From": booking.train.source,
                "Destination": booking.train.destination,
                "seats booked": booking.seats_booked,
                "total_price": booking.total_price,
                "confirmed": booking.confirmed
            }
            for booking in all_bookings
        ]
    
    def get_searches(self, user):
        collection = DATABASE['api_logs']
        searches = list(collection.find({ "user_id": user.id }).sort("timestamp", -1).limit(5))
        
        return [
            {
                "Source": search.get('search_filters', {}).get('source') or "Any",
                "Destination": search.get('search_filters', {}).get('destination') or "Any"
            }
            for search in searches
        ]
    
    class Meta:
        model = User
        fields = ['user_name', 'user_email', 'bookings', 'searches']
