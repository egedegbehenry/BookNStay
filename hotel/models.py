""" from django.db import models
from django.conf import settings 
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Room(models.Model):
    ROOM_CATEGORIES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUXE'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
        ('STE', 'SUITE'),
        ('EXE', 'EXECUTIVE'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    beds =models.IntegerField()
    capacity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.number}. {self.category} with {self.beds}beds for {self.capacity} people'
   
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'

    def get_room_category(self): 
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category
    
    def get_cancel_booking_url(self):
        return reverse_lazy('hotel:CancelBookingView', args=[self.pk, ]) """




""" 
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone

class Room(models.Model):
    DELUXE = 'DEL'
    KING = 'KIN'
    QUEEN = 'QUE'
    SUITE = 'STE'
    EXECUTIVE = 'EXE'
    SINGLE = 'SIN'

    ROOM_CATEGORIES = [
        (DELUXE, 'Deluxe'),
        (KING, 'King'),
        (QUEEN, 'Queen'),
        (SUITE, 'Suite'),
        (EXECUTIVE, 'Executive'),
        (SINGLE, 'Single'),
    ]

    number = models.PositiveIntegerField()
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    beds = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['number']

    def __str__(self):
        return f'Room {self.number} ({self.get_category_display()}) with {self.beds} beds for {self.capacity} people'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} booked {self.room} from {self.check_in} to {self.check_out}'

    def get_room_category(self):
        return self.room.get_category_display()

    def get_cancel_booking_url(self):
        return reverse_lazy('hotel:CancelBookingView', args=[self.pk])
 """