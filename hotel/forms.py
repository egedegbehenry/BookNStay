from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import RoomCategory, Person

#  input_formats=["%Y-%m-%dT%H:%M", ],