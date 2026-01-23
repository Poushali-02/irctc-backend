from rest_framework import serializers
from .models import Booking
from trains.models import Train

class TrainNestedSerializer(serializers.ModelSerializer):
    """
    Nested serializer for train details in booking responses
    """
    class Meta:
        model = Train
        fields = ['id', 'train_number', 'name', 'source', 'destination']

class BookingListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing user bookings with nested train details
    """
    train = TrainNestedSerializer(read_only=True)
    seats = serializers.IntegerField(source='seats_booked')
    
    class Meta:
        model = Booking
        fields = ['id', 'train', 'seats', 'booking_time', 'confirmed']

class BookingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for booking model
    """
    
    class Meta:
        model = Booking
        fields = [
            'id','train', 'seats_booked', 'booking_time', 'confirmed'
        ]
        read_only_fields = ['id', 'booking_time', 'confirmed']
        
    def validate(self, data):
        # seat available or not
        train = data['train']
        seats = data['seats_booked']
        
        if train.available_seats < seats:
            raise serializers.ValidationError(
                f"Only {train.available_seats} are available. Unable to assign {seats} seats."
            )
        return data