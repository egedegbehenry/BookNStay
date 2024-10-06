from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from hotel.models import Room, Booking
from django.utils import timezone

class HotelViewsTest(TestCase):

    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='testuser@example.com'
        )

        # Create a test room
        self.room = Room.objects.create(
            name='Deluxe Room', description='A deluxe room for testing.', price=100.00
        )

        # Create a test booking
        self.booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=timezone.now(),
            check_out=timezone.now() + timezone.timedelta(days=1),
            guests=2
        )

    # Test for login view
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/login.html')

        # Test login with valid credentials
        login = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(login, reverse('bookings'))

    # Test for logout view
    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/')
        self.assertFalse('_auth_user_id' in self.client.session)

    # Test for signup view
    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/signup.html')

        # Test signup post request
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
        })
        self.assertRedirects(response, reverse('booking_list'))

    # Test profile view
    def test_profile_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/profile.html')

    # Test profile edit view
    def test_profile_edit_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/profile_edit.html')

        # Test profile update
        response = self.client.post(reverse('profile_edit'), {
            'first_name': 'Updated', 'last_name': 'User',
            'email': 'updated@example.com'
        })
        self.assertRedirects(response, reverse('room_list'))

    # Test delete account view
    def test_delete_account_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/delete_account.html')

        # Test account deletion
        response = self.client.post(reverse('delete_account'), {'password': 'password123'})
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(User.objects.filter(username='testuser').count(), 0)

    # Test for room list view
    def test_room_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('room_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/room_list.html')
        self.assertContains(response, 'Deluxe Room')

    # Test room creation view (admin functionality)
    def test_room_create_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('room_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/room_form.html')

        # Test room creation post request
        response = self.client.post(reverse('room_create'), {
            'name': 'Test Room', 'description': 'Test room description', 'price': 50.00
        })
        self.assertRedirects(response, reverse('room_list'))
        self.assertTrue(Room.objects.filter(name='Test Room').exists())

    # Test room update view
    def test_room_update_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('room_update', kwargs={'pk': self.room.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/room_form.html')

        # Test room update post request
        response = self.client.post(reverse('room_update', kwargs={'pk': self.room.pk}), {
            'name': 'Updated Room', 'description': 'Updated description', 'price': 150.00
        })
        self.assertRedirects(response, reverse('room_list'))
        self.assertTrue(Room.objects.filter(name='Updated Room').exists())

    # Test room delete view
    def test_room_delete_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('room_delete', kwargs={'pk': self.room.pk}))
        self.assertRedirects(response, reverse('room_list'))
        self.assertFalse(Room.objects.filter(pk=self.room.pk).exists())

    # Test booking list view
    def test_booking_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('booking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/booking_list.html')
        self.assertContains(response, self.booking.room.name)

    # Test booking creation view
    def test_booking_create_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('booking_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/booking_form.html')

        # Test booking creation post request
        response = self.client.post(reverse('booking_create'), {
            'room': self.room.id,
            'check_in': timezone.now(),
            'check_out': timezone.now() + timezone.timedelta(days=2),
            'guests': 2
        })
        self.assertRedirects(response, reverse('booking_list'))

    # Test booking update view
    def test_booking_update_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('booking_update', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/manage_booking.html')

        # Test booking update post request
        response = self.client.post(reverse('booking_update', kwargs={'pk': self.booking.pk}), {
            'room': self.room.id,
            'check_in': timezone.now(),
            'check_out': timezone.now() + timezone.timedelta(days=2),
            'guests': 3
        })
        self.assertRedirects(response, reverse('booking_list'))
        self.assertEqual(Booking.objects.get(pk=self.booking.pk).guests, 3)

    # Test booking delete view
    def test_booking_delete_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('booking_delete', kwargs={'pk': self.booking.pk}))
        self.assertRedirects(response, reverse('bookings'))
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())
