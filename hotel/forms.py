from django import forms
from .models import Room, Booking

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'category', 'beds', 'capacity']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'room', 'check_in', 'check_out']
