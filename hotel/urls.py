""" from django.urls import path
from .views import RoomListView, BookingListView, RoomDetailView, CancelBookingView, CheckoutView, success_view, cancel_view, BookingFormView, contact_us

app_name = 'hotel'

urlpatterns = [

    path('', BookingFormView.as_view(), name='BookingFormView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    path('success/', success_view, name='success_view'),
    path('cancel/', cancel_view, name='cancel_view'),
    path('contact-us/', contact_us, name="contact_us")


]
 """




""" from django.urls import path
from .views import (
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView
)

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_add'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),

    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/add/', BookingCreateView.as_view(), name='booking_add'),
    path('bookings/<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_edit'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
]
 """