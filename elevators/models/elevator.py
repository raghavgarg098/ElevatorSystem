from .base import BaseModelMixin
from .elevator_system import ElevatorSystem

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Elevator(BaseModelMixin):
    ELEVATOR_STATUS_CHOICES = [
        ('MOVING_UP', 'Moving Up'),
        ('MOVING_DOWN', 'Moving Down'),
        ('NOT_WORKING', 'Not Working'),
        ('MAINTENANCE', 'Maintenance'),
        ('AVAILABLE', 'Available'),
    ]
    DOOR_STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSE', 'Close'),
    ]

    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ELEVATOR_STATUS_CHOICES)
    door_status = models.CharField(max_length=10, choices=DOOR_STATUS_CHOICES)
    current_floor = models.IntegerField()
    destination_floors = ArrayField(models.IntegerField(), default=list)

