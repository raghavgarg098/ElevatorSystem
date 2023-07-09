from django.http import JsonResponse

from ..models import Elevator, UserRequest

from ..serializers import ElevatorSerializer


class ElevatorManager:
    def __init__(self, elevator_id, elevator=None):
        self.elevator_id = elevator_id
        self._elevator = elevator

    @property
    def elevator(self):
        if self._elevator:
            return self._elevator
        self._elevator = Elevator.objects.get(id=self.elevator_id)
        return self._elevator

    def can_execute_action(self, action):
        can_exec_func = getattr(self, 'can_execute_' + action.lower(), None)
        if can_exec_func:
            return can_exec_func()
        return False

    def execute_action(self, action):
        exec_func = getattr(self, 'execute_' + action.lower(), None)
        if exec_func:
            exec_func()
            serializer = ElevatorSerializer(self.elevator)
            return JsonResponse(serializer.data, status=200)
        return JsonResponse({'error': 'Invalid action'}, status=400)

    def can_execute_move(self):
        return bool(self.elevator.destination_floors) and self.elevator.door_status == 'CLOSE'

    def execute_move(self):
        destination_floor = self.elevator.destination_floors[0]
        self.elevator.status = 'MOVING_UP' if destination_floor > self.elevator.current_floor else 'MOVING_DOWN'
        self.elevator.save()

        # Update the status of UserRequest objects in a single query
        UserRequest.objects.filter(
            elevator=self.elevator,
            status='INITIALIZED',
            destination_floor=self.elevator.current_floor
        ).update(status='PROCESSING')

    def can_execute_open_door(self):
        return self.elevator.status == 'AVAILABLE'

    def execute_open_door(self):
        self.elevator.door_status = 'OPEN'
        self.elevator.save()

    def can_execute_close_door(self):
        return self.elevator.status == 'AVAILABLE'

    def execute_close_door(self):
        self.elevator.door_status = 'CLOSE'
        self.elevator.save()

    def can_execute_mark_available(self):
        return True

    def execute_mark_available(self):
        self.elevator.status = 'AVAILABLE'
        self.elevator.save()

    def can_execute_mark_unavailable(self):
        return (
            self.elevator.destination_floors == [] and
            self.elevator.status == 'AVAILABLE'
        )

    def execute_mark_unavailable(self):
        self.elevator.status = 'UNAVAILABLE'
        self.elevator.save()

    def can_execute_reach_destination(self):
        return self.elevator.status in ['MOVING_UP', 'MOVING_DOWN'] and self.elevator.destination_floors

    def execute_reach_destination(self):
        self.elevator.current_floor = self.elevator.destination_floors[0]
        self.elevator.destination_floors = self.elevator.destination_floors[1:]
        self.elevator.status = 'AVAILABLE'
        self.elevator.save()

        # Update the status of UserRequest objects in a single query
        UserRequest.objects.filter(
            elevator=self.elevator,
            destination_floor=self.elevator.current_floor
        ).update(status='PROCESSED')
