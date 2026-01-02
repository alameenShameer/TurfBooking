from django.shortcuts import render, get_object_or_404
from .models import District, Location


def district_list(request):
    districts = District.objects.all()
    return render(
        request,
        'locations/district_list.html',
        {'districts': districts}
    )


def location_list(request, district_id):
    district = get_object_or_404(District, id=district_id)
    locations = district.locations.all()

    return render(
        request,
        'locations/location_list.html',
        {
            'district': district,
            'locations': locations
        }
    )
