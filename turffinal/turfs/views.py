from django.shortcuts import render, get_object_or_404, redirect
from .models import Turf
from locations.models import Location,District
from django.contrib.auth.decorators import login_required


def turf_list(request):
    turfs = Turf.objects.filter(is_active=True)
    return render(
        request,
        'turfs/turf_list.html',
        {'turfs': turfs}
    )


def turf_by_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    turfs = location.turfs.filter(is_active=True)

    return render(
        request,
        'turfs/turf_by_location.html',
        {
            'location': location,
            'turfs': turfs
        }
    )


def turf_detail(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)
    return render(
        request,
        'turfs/turf_detail.html',
        {'turf': turf}
    )

@login_required
def add_turf(request):
    if request.user.profile.role != "OWNER":
        return redirect("login")

    districts = District.objects.all()
    locations = Location.objects.none()

    district_id = request.GET.get("district")
    if district_id and district_id.isdigit():
        locations = Location.objects.filter(district_id=district_id)

    if request.method == "POST":
        location_id = request.POST.get("location")

        if not location_id:
            messages.error(request, "Please select a location")
            return redirect(request.path + f"?district={district_id}")

        Turf.objects.create(
            name=request.POST.get("name"),
            owner=request.user,
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            area_sqft=request.POST.get("area_sqft"),
            location_id=location_id,
            is_active=True
        )

        return redirect("turf_dashboard")

    return render(
        request,
        "turfs/add_turf.html",
        {
            "districts": districts,
            "locations": locations,
            "selected_district": district_id,
        }
    )
