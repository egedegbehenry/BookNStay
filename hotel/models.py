from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone


class Room(models.Model):
    DELUXE = 'DEL'
    KING = 'KIN'
    QUEEN = 'QUE'
    SUITE = 'STE'
    EXECUTIVE = 'EXE'
    SINGLE = 'SIN'

    AVAILABLE = 'AVAILABLE'
    PENDING = 'PENDING'
    BOOKED = 'BOOKED'
    UNAVAILABLE = 'UNAVAILABLE'


    ROOM_CATEGORIES = [
        (DELUXE, 'Deluxe'),
        (KING, 'King'),
        (QUEEN, 'Queen'),
        (SUITE, 'Suite'),
        (EXECUTIVE, 'Executive'),
        (SINGLE, 'Single'),
    ]

    ROOM_STATUS = [
        (AVAILABLE, 'Avaialable'),
        (PENDING, 'Pending'),
        (BOOKED, 'Booked'),
        (UNAVAILABLE, 'Unavailable')
    ]

    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    description = models.TextField(max_length=255)
    capacity = models.PositiveIntegerField()
    room_price = models.FloatField()
    number = models.CharField(max_length=50)
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    status = models.CharField(max_length=50, choices=ROOM_STATUS)
    star_rating = models.PositiveIntegerField()

    def __str__(self):
        return f'Room {self.number} ({self.get_category_display()})'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='Default Address')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Booking from {self.check_in} to {self.check_out}"
    def get_room_category(self):
        return self.room.get_category_display()

    def get_cancel_booking_url(self):
        return reverse_lazy('hotel:CancelBookingView', args=[self.pk])


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return f'Payment of {self.amount} by {self.user} on {self.payment_date}'
