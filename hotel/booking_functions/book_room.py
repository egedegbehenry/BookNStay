from hotel.models import Booking, Room


def book_room(request, room, check_in, check_out):
    booking = Booking.objects.create(
        user=request.user,
        room=room
        check_in=check_in
        check_out
    )
    booking.save()

    return booking