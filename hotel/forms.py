from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth import get_user_model
from .models import User, Room, Booking, Payment
from django.utils import timezone
from datetime import datetime

class SignupForm(UserCreationForm):
    """
    Form for user signup including username, password, email, and name fields.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        error_messages={'unique': 'A user with that username already exists.'}
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.fields['username'].error_messages['unique'], code='unique'
            )
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields didn't match.")
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating user information.
    """
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class RoomForm(forms.ModelForm):
    """
    Form for creating and updating room information.
    """
    class Meta:
        model = Room
        fields = [
            'category', 'description', 'capacity', 'room_price', 'number', 'status', 'star_rating'
        ]
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
    """
    Form for booking a room.
    """
    
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'room', 'name', 'address']
        widgets = {
            'check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.all()  # Add this line

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        today = timezone.now()  # This will give you an aware datetime

        if check_in and check_out:
            # Convert check_in and check_out to aware datetime
            check_in = timezone.make_aware(datetime.combine(check_in, timezone.datetime.min.time()))
            check_out = timezone.make_aware(datetime.combine(check_out, timezone.datetime.min.time()))

            if check_in >= check_out:
                self.add_error('check_out', 'Checkout date must be after check-in date.')
            if check_in < today:
                self.add_error('check_in', 'Check-in date cannot be in the past.')

        return cleaned_data

class PaymentForm(forms.ModelForm):
    """
    Form for processing payments.
    """
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


class CustomPasswordResetForm(PasswordResetForm):
    """
    Form for resetting user passwords.
    """
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )
