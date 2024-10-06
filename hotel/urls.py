from django.contrib.auth import views as auth_views
from django.urls import path
from .views import ( ProfileView, ProfileEditView, DeleteAccountView, contact_us, payment, book_now,
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView, SignupView,
    CustomLoginView, CustomLogoutView, CustomPasswordResetView,
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    # Password management URLs
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='hotel/password_change_form.html'
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
    
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    
    # Password reset URLs
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Profile management URLs
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    
    # Room CRUD URLs
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_add'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    
    # Booking CRUD URLs
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/add/', BookingCreateView.as_view(), name='booking_add'),
    path('bookings/<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_edit'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    
    # Other URLs
    path('book_now/', book_now, name='book_now'),
    path('contact_us/', contact_us, name='contact_us'),
    path('payment/', payment, name='payment'),
]
