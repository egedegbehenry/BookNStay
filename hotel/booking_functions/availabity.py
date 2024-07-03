import datetime
from hotel.models import Room, Booking


if form.is_valid():
            data = form.cleaned_data
        room_list = Room.objects.filter(category=category)
        available_rooms=[]
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
