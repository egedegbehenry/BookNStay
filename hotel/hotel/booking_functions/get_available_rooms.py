from hotel.models import Room, Booking
from .availability import check_avaiability
def get_available_rooms(category, check_in, check_out):
       
    room_list = Room.objects.filter(category=category)

    available_rooms=[]
    for room in room_list:
            
        if check_availability(room, check_in, check_out):
            available_rooms.append(room)

    if len(available_rooms) > 0:
        return available_rooms
    else:
        return None