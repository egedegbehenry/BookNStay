from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking
from .forms import AvailabilityForm
from hotel.booking_functions.availability import check_availability
from hotel.booking_functions.get_room_cat_url_list import get_room_cat_url_list
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


class RoomView(View):
    def get (self, request, *args, **kwargs):
        category = self.kwargs.get('category',None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
        
        if len (room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
        
            context ={
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category is not avaialable')

    
    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category',None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms=[]
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms)>0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Book another one')
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:BookingListView')
    
