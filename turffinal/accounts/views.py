from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Profile
from turfs.models import Turf
from booking.models import Booking, Slot
from locations.models import District, Location
from django.utils import timezone


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

def user_dashboard(request):
    user = request.user
    now = timezone.now()

    # BOOKING COUNTS
    total_bookings = Booking.objects.filter(user=user).count()
    upcoming_bookings = Booking.objects.filter(
        user=user,
        slot__start_time__gte=now
    ).count()
    completed_bookings = Booking.objects.filter(
        user=user,
        slot__start_time__lt=now
    ).count()

    # FILTER DATA
    selected_district = request.GET.get('district')
    selected_location = request.GET.get('location')

    districts = District.objects.all()
    locations = Location.objects.none()
    turfs = Turf.objects.all()

    if selected_district:
        locations = Location.objects.filter(district_id=selected_district)
        turfs = turfs.filter(location__district_id=selected_district)

    if selected_location:
        turfs = turfs.filter(location_id=selected_location)

    context = {
        'total_bookings': total_bookings,
        'upcoming_bookings': upcoming_bookings,
        'completed_bookings': completed_bookings,
        'districts': districts,
        'locations': locations,
        'turfs': turfs,
        'selected_district': selected_district,
        'selected_location': selected_location,
    }

    return render(request, 'accounts/user_dashboard.html', context)



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