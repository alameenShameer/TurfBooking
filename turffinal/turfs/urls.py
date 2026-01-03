from django.urls import path
from . import views

urlpatterns = [
    path('', views.turf_list, name='turf_list'),
    path(
        'location/<int:location_id>/',
        views.turf_by_location,
        name='turf_by_location'
    ),
    path(
        '<int:turf_id>/',
        views.turf_detail,
        name='turf_detail'
    ),
    path('add/', views.add_turf, name='add_turf'),
    path("get-locations/", views.get_locations, name="get_locations"),  # ✅ NEW
]


