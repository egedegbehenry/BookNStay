""" from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking
from .forms import AvailabilityForm
from hotel.booking_functions.availability import check_availability
from hotel.booking_functions.get_room_cat_url_list import get_room_cat_url_list
from hotel.booking_functions.get_room_category_human_format import get_room_category_human_format
from hotel.booking_functions.get_available_rooms import get_available_rooms
from hotel.booking_functions.book_room import book_room
# Create your views here.


def RoomListView(request):
    room_category_url_list = get_room_cat_url_list()

    context = {
        "room_list": room_category_url_list,
    }
    return render(request, 'room_list_view.html', context)

class BookingListView(ListView):
    model=Booking
    template_name="booking_list_view.html"


    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class RoomDetailView(View):
    def get (self, request, *args, **kwargs):
        category = self.kwargs.get('category',None)
        human_format_room_category = get_room_category_human_format (category)
        form = AvailabilityForm()
        human_format_room_category is not None:

        context ={
                'room_category': human_format_room_category,
                'form': form,
            }
        return render(request, 'room_detail_view.html', context)
    else:
        return HttpResponse('Category is not avaialable')

    
    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category',None)
        form = AvailabilityForm(request.POST)

        
        if form.is_valid():

           data = form.cleaned_data
        

        available_rooms = get_available_rooms (category, 
                                               data['check_in'], data['check_out'])

        if available_rooms is not None:
           booking = book_room(request, available_rooms[0], 
                               data['check_in'], data['check_out'])

        
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Book another one')
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:BookingListView')
    
 """








""" from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Room, Booking
from .forms import RoomForm, BookingForm

# Room Views
class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'hotel/room_form.html'
    success_url = reverse_lazy('room_list')

class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

# Booking Views
class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'

class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')
 """