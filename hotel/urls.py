from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy

from .views import (
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView
)

urlpatterns = [
    # Login and logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # Password change
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url=reverse_lazy('password_change_done')), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    #Rooms CRUD
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_add'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),

    
    #Bookings CRUD
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/add/', BookingCreateView.as_view(), name='booking_add'),
    path('bookings/<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_edit'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
]




   
