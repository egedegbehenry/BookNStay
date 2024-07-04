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