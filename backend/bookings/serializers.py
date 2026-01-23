from rest_framework import serializers
from .models import Booking

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