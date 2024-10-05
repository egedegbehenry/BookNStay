from hotel.models import Room
from django.urls import reverse

#function that returns Room Category and Category URL List


def get_room_cat_url_list():
    rooom = Room.objects.all()[0]     #Getting a Random "Room" object
    
    #Making a dictionary from  "ROOM CATEGORIES" Tuple on the "Room"   
    room_categories = dict(room.ROOM_CATEGORIES)                         

    room_cat_url_list = []  #Empty Room (Category, URL) list

    for category in room_categories:                                      #for loop for populating the room_cat_url_list  (cat = category)
        room_category = room_categories.get(category)
        room_url = reverse('hotel:RoomDetailView', Kwargs={
                            'category': category})
       
        room_cat_url_list.append((room_category, room_url))

    return room_cat_url_list