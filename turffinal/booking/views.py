from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from turfs.models import Turf
from .models import Slot, Booking

def turf_list(request):
    turfs = Turf.objects.filter(is_active=True)
    return render(request, 'booking/turf_list.html', {'turfs': turfs})

def turf_slots(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)
    slots = turf.slots.filter(is_active=True)

    return render(
        request,
        'booking/turf_slots.html',
        {
            'turf': turf,
            'slots': slots
        }
    )

@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)

    if request.method == 'POST':
        date = request.POST.get('date')

        try:
            Booking.objects.create(
                user=request.user,
                slot=slot,
                date=date
            )
            messages.success(request, 'Booking successful!')

        except IntegrityError:
            messages.error(
                request,
                'This slot is already booked for the selected date.'
            )

    return redirect('turf_slots', turf_id=slot.turf.id)

@login_required
def my_bookings(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related('slot__turf')
        .order_by('-date')
    )

    return render(
        request,
        'booking/my_bookings.html',
        {'bookings': bookings}
    )

@login_required
def add_slot(request, turf_id):
    turf = get_object_or_404(Turf, id=turf_id)

    # Only owner of the turf can add slots
    if turf.owner != request.user:
        return redirect("login")

    if request.method == "POST":
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        price = request.POST.get("price")

        Slot.objects.create(
            turf=turf,
            start_time=start_time,
            end_time=end_time,
            price=price
        )

        return redirect("turf_dashboard")

    return render(
        request,
        "booking/add_slot.html",
        {"turf": turf}
    )

from django.http import HttpResponseForbidden

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.slot.turf.owner != request.user:
        return HttpResponseForbidden("You are not allowed to approve this booking")

    booking.status = "CONFIRMED"
    booking.save()

    messages.success(request, "Booking confirmed")
    return redirect("turf_dashboard")



@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.slot.turf.owner != request.user:
        return HttpResponseForbidden("You are not allowed to approve this booking")

    booking.status = "CANCELLED"
    booking.save()

    messages.success(request, "Booking is cancelled")
    return redirect("turf_dashboard")
