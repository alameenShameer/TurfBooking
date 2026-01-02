from django.db import models
from django.conf import settings
from turfs.models import Turf


class Slot(models.Model):
    turf = models.ForeignKey(
        Turf,
        on_delete=models.CASCADE,
        related_name='slots'
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.turf.name} | {self.start_time} - {self.end_time}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    slot = models.ForeignKey(
        Slot,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('slot', 'date')

    def __str__(self):
        return f"{self.user} | {self.slot} | {self.date}"
