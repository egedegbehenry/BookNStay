from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from hotel.forms import SignupForm, CustomUserChangeForm, RoomForm, BookingForm, PaymentForm, CustomPasswordResetForm
from hotel.models import User, Room, Booking, Payment

class FormTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@example.com',
            password='testpass123', 
            first_name='Test', 
            last_name='User'
        )
        self.room = Room.objects.create(
            category='Deluxe', 
            description='Spacious room', 
            capacity=2, 
            room_price=150.0, 
            number='101', 
            status='available', 
            star_rating=5
        )
    
    def test_signup_form_valid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_signup_form_invalid_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'differentpass',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        # Correct the single apostrophe mismatch
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])
    
    def test_custom_user_change_form_valid(self):
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        form = CustomUserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_room_form_valid(self):
        form_data = {
            'category': 'Deluxe',
            'description': 'Updated description',
            'capacity': 2,
            'room_price': 200.0,
            'number': '102',
            'status': 'available',
            'star_rating': 5
        }
        form = RoomForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_booking_form_valid(self):
        form_data = {
            'check_in': (timezone.now() + timedelta(days=1)).date(),
            'check_out': (timezone.now() + timedelta(days=2)).date(),
            'room': self.room.id,
            'name': 'John Doe',
            'address': '123 Main St'
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_booking_form_invalid_past_check_in(self):
        form_data = {
            'check_in': (timezone.now() - timedelta(days=1)).date(),
            'check_out': (timezone.now() + timedelta(days=1)).date(),
            'room': self.room.id,
            'name': 'John Doe',
            'address': '123 Main St'
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['check_in'], ['Check-in date cannot be in the past.'])
    
    def test_payment_form_valid(self):
        # Create a booking instance
        booking = Booking.objects.create(
            check_in=timezone.now() + timedelta(days=1),
            check_out=timezone.now() + timedelta(days=3),
            room=self.room,
            name='John Doe',
            address='123 Main St'
        )
        form_data = {
            'booking': booking.id,
            'user': self.user.id,  # Correct user field provided
            'amount': 300.0,
            'payment_date': timezone.now().date(),
            'payment_method': 'Credit Card'
        }
        form = PaymentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_custom_password_reset_form_invalid_email(self):
        form_data = {'email': 'nonexistent@example.com'}
        form = CustomPasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())  # Should now return False

    def test_custom_password_reset_form_invalid_email(self):
        form_data = {'email': 'nonexistent@example.com'}
        form = CustomPasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())
