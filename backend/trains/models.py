from django.db import models

# Create your models here.
class Train(models.Model):
    """Train model for storing train information"""
    train_number = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=155)
    source = models.CharField(max_length=155)
    destination = models.CharField(max_length=155)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'train'
        ordering = ['train_number']
        indexes = [
            models.Index(fields=['source', 'destination']),
            models.Index(fields=['train_number']),
        ]
    
    def __str__(self):
        return f"{self.train_number} - {self.name}"