from django.shortcuts import render, get_object_or_404
from .models import District, Location
from django.http import JsonResponse


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
def get_locations(request):
    district_id = request.GET.get("district")

    if not district_id:
        return JsonResponse([], safe=False)

    locations = Location.objects.filter(
        district__id=district_id
    ).values("id", "name")

    return JsonResponse(list(locations), safe=False)