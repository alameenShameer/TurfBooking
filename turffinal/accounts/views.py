from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Profile
from turfs.models import Turf
from booking.models import Booking


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Superuser (Admin)
            if user.is_superuser:
                return redirect("/admin/")

            profile = user.profile

            # Turf Owner
            if profile.role == "OWNER":
                return redirect("turf_dashboard")

            # Normal User
            return redirect("user_dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("login")
    return render(request, "accounts/admin_dashboard.html")

@login_required
def turf_dashboard(request):
    if request.user.profile.role != "OWNER":
        return HttpResponseForbidden("Only turf owners allowed")

    turfs = Turf.objects.filter(owner=request.user)

    bookings = (
        Booking.objects
        .filter(slot__turf__owner=request.user)
        .select_related("slot", "slot__turf", "user")
        .order_by("-date")
    )

    return render(
        request,
        "accounts/turf_dashboard.html",
        {
            "turfs": turfs,
            "bookings": bookings,
        }
    )

from locations.models import District, Location

@login_required
def user_dashboard(request):
    if request.user.profile.role != "USER":
        return redirect("login")

    districts = District.objects.all()
    locations = Location.objects.none()
    turfs = Turf.objects.filter(is_active=True)

    district_id = request.GET.get("district")
    location_id = request.GET.get("location")

    if district_id:
        locations = Location.objects.filter(district_id=district_id)
        turfs = turfs.filter(location__district_id=district_id)

    if location_id:
        turfs = turfs.filter(location_id=location_id)

    return render(
        request,
        "accounts/user_dashboard.html",
        {
            "turfs": turfs,
            "districts": districts,
            "locations": locations,
            "selected_district": district_id,
            "selected_location": location_id,
        }
    )



def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('user_signup')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.profile.role = 'USER'
        user.profile.save()

        login(request, user)
        return redirect('user_dashboard')

    return render(request, 'accounts/user_signup.html')

def owner_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('owner_signup')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.profile.role = 'OWNER'
        user.profile.save()

        login(request, user)
        return redirect('turf_dashboard')

    return render(request, 'accounts/owner_signup.html')

def turf_dashboard(request):
    # get tab from URL (?tab=...)
    tab = request.GET.get('tab', 'dashboard')

    turfs = Turf.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(slot__turf__owner=request.user)

    context = {
        'tab': tab,
        'turfs': turfs,
        'bookings': bookings,
    }

    return render(request, 'accounts/turf_dashboard.html', context)