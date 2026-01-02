from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('OWNER', 'Turf Owner'),
    )

    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="profile"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='USER'
    )

    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
