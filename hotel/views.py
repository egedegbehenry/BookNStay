from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import DeleteView
from .models import Room, Booking
from .forms import RoomForm, BookingForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

def home(request):
    return render(request, 'hotel/home.html')

# Login view
class CustomLoginView(LoginView):
    template_name = 'hotel/login.html' 
    success_url = reverse_lazy('home') 

# Logout view
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # Redirect to home page after logout

def room_delete_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room has been deleted successfully.')
        return redirect('room_list')
    return render(request, 'hotel/room_confirm_delete.html', {'object': room})
 
# Password reset request view
class CustomPasswordResetView(PasswordResetView):
    template_name = 'hotel/password_reset_form.html'  # Your custom password reset form template
    email_template_name = 'hotel/password_reset_email.html'  # Your custom password reset email template
    success_url = reverse_lazy('password_reset_done')  # Redirect to password reset done view upon success

# Password reset done view
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'hotel/password_reset_done.html'  # Your custom password reset done template

# Password reset confirm view
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'hotel/password_reset_confirm.html'  # Your custom password reset confirm template
    success_url = reverse_lazy('password_reset_complete')  # Redirect to password reset complete view upon success

# Password reset complete view
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'hotel/password_reset_complete.html'  # Your custom password reset complete template


# Room Views
class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'hotel/room_form.html'
    success_url = reverse_lazy('room_list')

class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

# Booking Views
class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'

class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')