from django.db import models
from django.conf import settings
from locations.models import Location


class Turf(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_turfs'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='turfs'
    )

    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    area_sqft = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)  # ✅ ADD THIS

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

