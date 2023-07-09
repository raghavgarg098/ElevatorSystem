from rest_framework import serializers
from ..models import Elevator


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = ('status',
                  'door_status',
                  'current_floor',
                  'destination_floors')

