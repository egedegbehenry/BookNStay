from django.urls import reverse, resolve
from django.test import SimpleTestCase
from hotel.views import (
    SignupView, CustomLoginView, CustomLogoutView, CustomPasswordResetView,
    ProfileView, ProfileEditView, DeleteAccountView, RoomListView, 
    BookingListView, contact_us, book_now, payment
)

class UrlsTest(SimpleTestCase):
    
    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignupView)
    
    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)
    
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, CustomLogoutView)
    
    def test_password_reset_url(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, CustomPasswordResetView)
    
    def test_profile_url(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)
    
    def test_profile_edit_url(self):
        url = reverse('profile_edit')
        self.assertEqual(resolve(url).func.view_class, ProfileEditView)
    
    def test_delete_account_url(self):
        url = reverse('delete_account')
        self.assertEqual(resolve(url).func.view_class, DeleteAccountView)
    
    def test_rooms_list_url(self):
        url = reverse('room_list')
        self.assertEqual(resolve(url).func.view_class, RoomListView)
    
    def test_bookings_list_url(self):
        url = reverse('booking_list')
        self.assertEqual(resolve(url).func.view_class, BookingListView)
    
    def test_contact_us_url(self):
        url = reverse('contact_us')
        self.assertEqual(resolve(url).func, contact_us)

    def test_book_now_url(self):
        url = reverse('book_now')
        self.assertEqual(resolve(url).func, book_now)

    def test_payment_url(self):
        url = reverse('payment')
        self.assertEqual(resolve(url).func, payment)
