from django.db import models


class Location(models.Model):
    city = models.CharField(blank=False, null=False)
    state = models.CharField(blank=False, null=False)
    longitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=4)
    latitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=4)