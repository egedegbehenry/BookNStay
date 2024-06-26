from django.urls import path
from .views import RoomListView, BookingList, BookingView, RoomDetailView

app_name = 'hotel'

urlpatterns = [
    path('room_list/', RoomList.as_view(), name='RoomList'),
    path('booking_list/', BookList.as_view(), name='BookingList'),
    path('book/', BookingView.as_view(), name='bookingView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),

]