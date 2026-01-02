from django.contrib import admin
from .models import District, Location


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district')
    list_filter = ('district',)
    search_fields = ('name',)
