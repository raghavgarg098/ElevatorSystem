from django.contrib import admin
from .models import Elevator, ElevatorSystem, UserRequest

# Register your models here.
admin.site.register(Elevator)
admin.site.register(ElevatorSystem)
admin.site.register(UserRequest)

