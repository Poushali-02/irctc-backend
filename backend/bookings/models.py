from django.db import models
from user.models import User
from trains.models import Train

# Create your models here.
class Booking(models.Model):
    """Booking model for storing train booking information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="bookings")
    seats_booked = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'booking'
        ordering = ['-booking_time']
    
    def __str__(self):
        return f"Booking {self.id} by {self.user.email} on {self.train.train_number}"