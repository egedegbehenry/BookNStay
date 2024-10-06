"""
Views for the hotel application.
"""

import logging
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordResetDoneView, 
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Room, Booking
from .forms import RoomForm, BookingForm, SignupForm, PaymentForm, CustomUserChangeForm
from django.utils import timezone

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    """
    Custom login view that redirects to bookings after successful login.
    """
    template_name = 'hotel/login.html'
    success_url = reverse_lazy('bookings')

class CustomLogoutView(LoginRequiredMixin, View):
    """
    Custom logout view that logs the user out and redirects to home.
    """
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out.')
        return HttpResponseRedirect('/')

    def clear_message(self, request):
        request.session['success_message'] = ''
        return JsonResponse({'status': 'message-cleared'})

class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view.
    """
    template_name = 'hotel/password_reset_form.html'
    email_template_name = 'hotel/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Custom password reset done view.
    """
    template_name = 'hotel/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom password reset confirm view.
    """
    template_name = 'hotel/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Custom password reset complete view.
    """
    template_name = 'hotel/password_reset_complete.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User profile view.
    """
    template_name = 'hotel/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    View for editing user profile.
    """
    form_class = CustomUserChangeForm
    template_name = 'hotel/profile_edit.html'
    success_url = reverse_lazy('room_list')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile. Please correct the errors.')
        return super().form_invalid(form)

class DeleteAccountView(LoginRequiredMixin, View):
    """
    View for deleting user account.
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'hotel/delete_account.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.POST.get('password')
        if user.check_password(password):
            username = user.username
            user.delete()
            messages.success(request, f'Your account ({username}) has been deleted.')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Account not deleted.')
            return redirect('delete_account')

def home(request):
    """
    Home page view.
    """
    return render(request, 'hotel/home.html')

class SignupView(View):
    """
    View for user signup.
    """
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
                return redirect(reverse('booking_list'))
            else:
                messages.error(request, 'Error logging in after signup. Please try logging in manually.')
                return redirect(reverse('login'))
        else:
            messages.error(request, 'Error with your signup. Please correct the errors below.')
            return render(request, self.template_name, {'form': form})

def contact_us(request):
    """
    Contact us page view.
    """
    if request.method == 'POST':
        # Handle form submission (if any)
        pass
    return render(request, 'hotel/contact_us.html')

class RoomListView(LoginRequiredMixin, ListView):
    """
    View for listing all rooms.
    """
    model = Room
    template_name = 'hotel/room_list.html'
    context_object_name = 'rooms'

class RoomCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new room.
    """
    model = Room
    form_class = RoomForm
    template_name = 'hotel/room_form.html'
    success_url = reverse_lazy('room_list')

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing room.
    """
    model = Room
    form_class = RoomForm
    template_name = 'hotel/room_form.html'
    success_url = reverse_lazy('room_list')

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a room.
    """
    model = Room
    template_name = 'hotel/room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

@login_required
def room_delete_view(request, pk):
    """
    Custom view for deleting a room.
    """
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room has been deleted successfully.')
        return redirect('room_list')
    return render(request, 'hotel/room_confirm_delete.html', {'object': room})

class BookingListView(LoginRequiredMixin, ListView):
    """
    View for listing all bookings.
    """
    model = Booking
    template_name = 'hotel/booking_list.html'
    context_object_name = 'bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for booking in context['bookings']:
            logger.info("Booking PK: %d, Check-in: %s, Check-out: %s", booking.pk, booking.check_in, booking.check_out)
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=self.request.user)

class BookingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for creating a new booking.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'hotel/booking_form.html'
    success_url = reverse_lazy('booking_list')
    success_message = "Booking successful! Your room has been reserved."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD
        return context

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your booking. Please correct the errors below.')
        return super().form_invalid(form)

class BookingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating an existing booking.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'hotel/manage_booking.html'
    success_url = reverse_lazy('booking_list')
    success_message = "Booking was updated successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD
        return context
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return redirect('booking_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the booking.")
        return super().form_invalid(form)

class BookingDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    View for deleting a booking.
    """
    model = Booking
    template_name = 'hotel/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings')
    success_message = "Booking was deleted successfully."

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return render(request, 'hotel/access_denied.html', status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('_save'):
            return self.form_valid(self.get_form())
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.get_object()
        return context

@login_required
def payment(request):
    """
    View for handling payments.
    """
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process payment logic
            return redirect('home')
    else:
        form = PaymentForm()
    return render(request, 'hotel/payment.html', {'form': form})

@login_required
def book_now(request):
    """
    Custom view to handle booking process based on login status.
    """
    if request.user.is_authenticated:
        return redirect('booking_list')
    else:
        return redirect('signup')

@login_required
def manage_bookings(request):
    """
    View for managing bookings.
    """
    return render(request, 'hotel/manage_bookings.html')

@login_required
def cancel_booking(request, pk):
    """
    View for cancelling a booking.
    """
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('booking_list')
    return render(request, 'hotel/cancel_booking.html', {'booking': booking})
