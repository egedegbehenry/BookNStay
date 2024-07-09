from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View 
from .models import Room, Booking
from .forms import RoomForm, BookingForm, SignupForm 
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BookingForm, PaymentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

# View for the home page
def home(request):
    return render(request, 'hotel/home.html')

# View for the signup page
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('booking_form')
    else:
        form = SignupForm()
    return render(request, 'hotel/signup.html', {'form': form})

# View for the booking form
@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Process booking logic
            return redirect('payment')
    else:
        form = BookingForm()
    return render(request, 'hotel/booking_form.html', {'form': form})

# View for the payment form
@login_required
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process payment logic
            return redirect('home')
    else:
        form = PaymentForm()
    return render(request, 'hotel/payment.html', {'form': form})

# Custom view to handle booking process based on login status
def book_now(request):
    if request.user.is_authenticated:
        return redirect('booking_list')
    else:
        return redirect('signup')

def home(request):
    return render(request, 'hotel/home.html')

class SignupView(View):
    template_name = 'hotel/signup.html'

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                request.session['success_message'] = 'Successfully Signed up.'
                request.session['first_name'] = form.cleaned_data.get('first_name')
                return redirect(reverse('task_list'))
            else:
                request.session['error_message'] = 'There was an error logging you in after signup. Please try logging in manually.'
                return redirect(reverse('login'))
        else:
            request.session['error_message'] = 'There was an error with your signup. Please correct the errors below.'
            return render(request, self.template_name, {'form': form})

def contact_us(request):
    if request.method == 'POST':
        # Handle form submission (if any)
        pass
    
    return render(request, 'hotel/contact_us.html')

# Login view
class CustomLoginView(LoginView):
    template_name = 'hotel/login.html' 
    success_url = reverse_lazy('room_list') 

# Logout view
class CustomLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out.')
        return HttpResponseRedirect('/')

    def clear_message(request):
        request.session['success_message'] = ''
        return JsonResponse({'status': 'message-cleared'}) # Redirect to home page after logout
 
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
    template_name = 'hotel/room_list.html'
    context_object_name = 'rooms'


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'hotel/room_form.html'
    success_url = reverse_lazy('room_list')

class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'hotel/room_form.html'
    success_url = reverse_lazy('room_list')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'hotel/room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

def room_delete_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room has been deleted successfully.')
        return redirect('room_list')
    return render(request, 'hotel/room_confirm_delete.html', {'object': room})

# Booking Views
from django.views.generic import ListView
from .models import Booking

class BookingListView(ListView):
    model = Booking
    template_name = 'hotel/booking_list.html'
    context_object_name = 'bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = context['bookings']
        for booking in bookings:
            print(f"Booking PK: {booking.pk}, Check-in: {booking.check_in}, Check-out: {booking.check_out}")  # Debugging line
        return context


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'hotel/booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'hotel/booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'hotel/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')