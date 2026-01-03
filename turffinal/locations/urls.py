from django.urls import path
from . import views

urlpatterns = [
    path('districts/', views.district_list, name='district_list'),
    path(
        'districts/<int:district_id>/locations/',
        views.location_list,
        name='location_list'
    ),
    path("get-locations/", views.get_locations, name="get_locations"),
]
