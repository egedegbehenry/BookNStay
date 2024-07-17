from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import Room, Booking
from .forms import RoomForm, BookingForm, SignupForm, PaymentForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView

# Account views
class CustomLoginView(LoginView):
    template_name = 'hotel/login.html'
    success_url = reverse_lazy('room_list')

class CustomLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out.')
        return HttpResponseRedirect('/')

    def clear_message(request):
        request.session['success_message'] = ''
        return JsonResponse({'status': 'message-cleared'})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'hotel/password_reset_form.html'
    email_template_name = 'hotel/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'hotel/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'hotel/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'hotel/password_reset_complete.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'hotel/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
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

# Home View
def home(request):
    return render(request, 'hotel/home.html')

# Signup and Contact Views
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
                return redirect(reverse('booking_list'))
            else:
                messages.error(request, 'Error logging in after signup. Please try logging in manually.')
                return redirect(reverse('login'))
        else:
            messages.error(request, 'Error with your signup. Please correct the errors below.')
            return render(request, self.template_name, {'form': form})

def contact_us(request):
    if request.method == 'POST':
        # Handle form submission (if any)
        pass
    return render(request, 'hotel/contact_us.html')

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
class BookingListView(ListView):
    model = Booking
    template_name = 'hotel/booking_list.html'
    context_object_name = 'bookings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for booking in context['bookings']:
            print(f"Booking PK: {booking.pk}, Check-in: {booking.check_in}, Check-out: {booking.check_out}")
        return context

class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'hotel/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        # Assign the current user to the booking before saving
        booking = form.save(commit=False)
        booking.user = self.request.user  # Assuming you have a 'user' field in your Booking model
        booking.save()
        
        messages.success(self.request, 'Booking successful! Your room has been reserved.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handling form errors
        messages.error(self.request, 'There was an error with your booking. Please correct the errors below.')
        return super().form_invalid(form)
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'hotel/booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'hotel/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')

# Payment View
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
