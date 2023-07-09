from .base import BaseModelMixin
from django.db import models


class ElevatorSystem(BaseModelMixin):
    elevators_number = models.IntegerField()
    max_queue_size = models.IntegerField()
