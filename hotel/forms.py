from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Room, Booking, Payment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['description', 'capacity', 'price', 'number', 'category', 'status', 'star_rating']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'star_rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'room', 'name', 'address', 'checkin_time', 'checkout_time', 'room_price']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'checkin_time': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'checkout_time': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'room_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }