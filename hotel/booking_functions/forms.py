from django import forms

class AvailabilityForm(forms.Form):
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES)