from django.urls import path
from . import views

urlpatterns = [
    path('turfs/', views.turf_list, name='turf_list'),
    path('turfs/<int:turf_id>/slots/', views.turf_slots, name='turf_slots'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path("add-slot/<int:turf_id>/", views.add_slot, name="add_slot"),
    path("confirm/<int:booking_id>/", views.confirm_booking, name="confirm_booking"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),


]
