from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='locations'
    )

    def __str__(self):
        return f"{self.name} ({self.district.name})"
