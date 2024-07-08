from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy
from . import views

from .views import (
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView, SignupView 
)

from hotel.views import (
    CustomLoginView, CustomLogoutView, CustomPasswordResetView,
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

"""
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
    path('signup/', SignupView.as_view(), name='signup'), 
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),  
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'), #Not working 
    path('password-reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),   #Not working 
 
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
"""

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('booking/', views.booking, name='booking'),
    path('payment/', views.payment, name='payment'),
    path('book_now/', views.book_now, name='book_now'),
    path('login/', auth_views.LoginView.as_view(template_name='hotel/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='hotel/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='hotel/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='hotel/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='hotel/password_reset_complete.html'), name='password_reset_complete'),
]




   
