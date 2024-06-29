from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import RoomCategory, Person

#  input_formats=["%Y-%m-%dT%H:%M", ],

class AvailabilityForm(forms.Form):

    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    room_category = forms.ModelChoiceField(
        queryset=RoomCategory.objects.all())
    #  widget=forms.Select(attrs={"class": "mdb-select md-form"})