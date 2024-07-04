from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(max_length=225, unique=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username


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

    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    description = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.CharField(max_length=50)
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    status = models.CharField(max_length=50)
    star_rating = models.PositiveIntegerField()

    def __str__(self):
        return f'Room {self.number} ({self.get_category_display()})'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    checkin_time = models.DateField()
    checkout_time = models.DateField()
    room_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} booked Room {self.room.number} from {self.checkin_time} to {self.checkout_time}'

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
