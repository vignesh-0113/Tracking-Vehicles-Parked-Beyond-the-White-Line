from django.db import models

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=100)
    license = models.CharField(max_length=100, default='UNKNOWN')
    detection_time = models.DateTimeField()

    def __str__(self):
        return f'{self.vehicle_number} at {self.detection_time}'
