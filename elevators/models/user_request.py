from .base import BaseModelMixin
from .elevator import Elevator

from django.db import models


class UserRequest(BaseModelMixin):
    REQUEST_STATUS_CHOICES = [
        ('INITIALIZED', 'Initialized'),
        ('NEGLECTED', 'Neglected'),
        ('PROCESSING', 'Processing'),
        ('PROCESSED', 'Processed'),
    ]

    current_floor = models.IntegerField()
    destination_floor = models.IntegerField()
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES)
    elevator = models.ForeignKey(Elevator, on_delete=models.SET_NULL, null=True)
