from django.urls import path
from .views import RoomLisView. BookingList, BookingView, RoomDetaillView

app_name = 'hotel'

urlpatterns = [
    path('room_list/', RoomLisView.as_view, name='RoomList'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    path('book/', BookingView.as_view(), name='BookingView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailsView')


]
