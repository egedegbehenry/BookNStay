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
        fields = ['category', 'description', 'capacity', 'room_price', 'number',  'status', 'star_rating']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'room_price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'star_rating': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'room', 'name', 'address', 'checkin_time', 'checkout_time']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'checkin_time': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'checkout_time': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in >= check_out:
                self.add_error('check_out', 'Checkout date must be after check-in date.')

        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['booking', 'user', 'amount', 'payment_date', 'payment_method']
        widgets = {
            'booking': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
        }
