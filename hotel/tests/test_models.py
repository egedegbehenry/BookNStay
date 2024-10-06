from django.test import TestCase
from django.contrib.auth.models import User
from hotel.models import Room, Booking, Payment
from django.utils import timezone
from datetime import timedelta

class RoomModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.room = Room.objects.create(
            description='A deluxe room with a view',
            capacity=2,
            room_price=150.00,
            number='101',
            category=Room.DELUXE,
            status=Room.AVAILABLE,
            star_rating=5,
            user=self.user
        )
    
    def test_room_creation(self):
        self.assertEqual(self.room.description, 'A deluxe room with a view')
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.room_price, 150.00)
        self.assertEqual(self.room.number, '101')
        self.assertEqual(self.room.category, Room.DELUXE)
        self.assertEqual(self.room.status, Room.AVAILABLE)
        self.assertEqual(self.room.star_rating, 5)
        self.assertEqual(str(self.room), 'Room 101 (Deluxe)')
    
class BookingModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.room = Room.objects.create(
            description='A deluxe room with a view',
            capacity=2,
            room_price=150.00,
            number='101',
            category=Room.DELUXE,
            status=Room.AVAILABLE,
            star_rating=5,
            user=self.user
        )
        self.check_in = timezone.now() + timedelta(days=1)
        self.check_out = timezone.now() + timedelta(days=3)
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            name='John Doe',
            address='123 Main St',
            check_in=self.check_in,
            check_out=self.check_out
        )
    
    def test_booking_creation(self):
        self.assertEqual(self.booking.name, 'John Doe')
        self.assertEqual(self.booking.address, '123 Main St')
        self.assertEqual(self.booking.room, self.room)
        self.assertEqual(str(self.booking), f'Booking from {self.check_in} to {self.check_out}')
    
    def test_room_category(self):
        self.assertEqual(self.booking.get_room_category(), 'Deluxe')

class PaymentModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.room = Room.objects.create(
            description='A deluxe room with a view',
            capacity=2,
            room_price=150.00,
            number='101',
            category=Room.DELUXE,
            status=Room.AVAILABLE,
            star_rating=5,
            user=self.user
        )
        self.check_in = timezone.now() + timedelta(days=1)
        self.check_out = timezone.now() + timedelta(days=3)
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            name='John Doe',
            address='123 Main St',
            check_in=self.check_in,
            check_out=self.check_out
        )
        self.payment = Payment.objects.create(
            booking=self.booking,
            user=self.user,
            amount=300.00,
            payment_date=timezone.now().date(),
            payment_method='Credit Card'
        )
    
    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, 300.00)
        self.assertEqual(self.payment.payment_method, 'Credit Card')
        self.assertEqual(str(self.payment), f'Payment of {self.payment.amount} by {self.user} on {self.payment.payment_date}')
