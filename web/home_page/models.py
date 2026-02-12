from django.db import models


class Location(models.Model):
    city = models.CharField(blank=False, null=False)
    state = models.CharField(blank=False, null=False)
    longitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5)
    latitude = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=4)

    def __str__(self):
        return f'{self.city.title()}, {self.state.upper()}'


class Temperature(models.Model):
    city = models.ForeignKey(Location, on_delete=models.CASCADE)
    temp = models.IntegerField(blank=False, null=False)
    hour = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f'{self.hour} - {self.temp}'
    

class Precipitation(models.Model):
    city = models.ForeignKey(Location, on_delete=models.CASCADE)
    probability = models.IntegerField(blank=False, null=False)
    day = models.DateField(blank=False, null=False)