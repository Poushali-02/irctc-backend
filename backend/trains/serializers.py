from rest_framework import serializers
from .models import Train

class TrainDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for train model
    """
    
    class Meta:
        model = Train
        fields = [
            'id','train_number','name', 
            'source', 'destination', 'departure_time',
            'arrival_time', 'total_seats','available_seats'
        ]