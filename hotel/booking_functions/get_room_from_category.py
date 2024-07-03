
def get_room_from_category(category):

    room_list = Room.objects.filter(category=category)
        
    if len (room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            return room_category
    else:
          return None
        
        