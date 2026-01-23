
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db import transaction
from .models import Booking
from .serializers import BookingDetailSerializer
from trains.models import Train

@extend_schema(tags=['Bookings'])
class BookingsCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    
    # authenticated user can create a booking only
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            train = serializer.validated_data['train']
            train = Train.objects.select_for_update().get(pk=train.pk)
            
            seats_booked = serializer.validated_data['seats_booked']
            
            if train.available_seats < seats_booked:
                return Response(
                    {"error": f"Only {train.available_seats} seats available, you requested {seats_booked}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            train.available_seats -= seats_booked
            train.save()
            
            booking = serializer.save(user=self.request.user)
            
            return Response (
                {
                    "booking":{
                        "id": booking.id,
                        "train": booking.train.id,
                        "seats_booked": booking.seats_booked
                    }
                },
                status=status.HTTP_201_CREATED
            )
            
            
@extend_schema(tags=['Bookings'])
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    
    # user needs to be authenticated
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).select_related("train", "user")