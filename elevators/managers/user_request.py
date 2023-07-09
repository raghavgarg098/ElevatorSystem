from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.models.functions import Abs, Length
from django.db.models.expressions import RawSQL

from ..models import UserRequest, ElevatorSystem, Elevator


class UserRequestManager:
    def __init__(self, current_floor, destination_floor, elevator_system_id):
        self.current_floor = current_floor
        self.destination_floor = destination_floor
        self.elevator_system_id = elevator_system_id
        self._existing_user_request = None
        self.elevator_system = self.get_elevator_system()

    @property
    def existing_user_request(self):
        if self._existing_user_request:
            return self._existing_user_request
        self._existing_user_request = UserRequest.objects.filter(
            current_floor=self.current_floor,
            destination_floor=self.destination_floor,
            status='INITIALIZED',
            elevator__elevator_system_id=self.elevator_system_id
        ).first()

        return self._existing_user_request

    def get_elevator_system(self):
        try:
            elevator_system = ElevatorSystem.objects.get(id=self.elevator_system_id)
        except ElevatorSystem.DoesNotExist:
            raise ValidationError("Invalid elevator system ID.")
        return elevator_system

    def assign_user_request(self):
        if self.existing_user_request:
            return JsonResponse({
                'user_request_id': self.existing_user_request.id,
                'status': self.existing_user_request.status,
                'elevator_id': self.existing_user_request.elevator_id
            })

        optimal_elevator = self.find_optimal_elevator()

        if optimal_elevator:
            # Mark the user request as initialized
            new_user_request = UserRequest.objects.create(
                current_floor=self.current_floor,
                destination_floor=self.destination_floor,
                elevator=optimal_elevator,
                status='INITIALIZED'
            )
            self.assign_floors_to_elevator(optimal_elevator)
        else:
            # Mark the user request as neglected
            new_user_request = UserRequest.objects.create(
                current_floor=self.current_floor,
                destination_floor=self.destination_floor,
                status='NEGLECTED'
            )

        return JsonResponse({
            'user_request_id': new_user_request.id,
            'status': new_user_request.status,
            'elevator_id': new_user_request.elevator_id
        })

    def find_optimal_elevator(self):
        available_elevator = self.find_nearest_elevator()
        if available_elevator:
            return available_elevator
        opposite_direction_elevator = self.find_opposite_direction_elevators()
        return opposite_direction_elevator

    def find_nearest_elevator(self):
        direction = 'MOVING_UP' if self.destination_floor > self.current_floor else 'MOVING_DOWN'

        moving_elevators = Elevator.objects.filter(
            elevator_system=self.elevator_system,
            status__in=[direction, 'AVAILABLE'],
            current_floor__lte=self.current_floor
        ).annotate(floor_difference=Abs(self.current_floor - F('current_floor'))).order_by('floor_difference')

        moving_elevators = moving_elevators.annotate(
            destination_floors_length=RawSQL('CARDINALITY(destination_floors)', ())
        ).filter(destination_floors_length__lt=self.elevator_system.max_queue_size)

        if moving_elevators.exists():
            return moving_elevators.first()

        return None

    def find_opposite_direction_elevators(self):
        opposite_direction_elevators = Elevator.objects.filter(
            elevator_system=self.elevator_system,
            status='MOVING_DOWN' if self.destination_floor > self.current_floor else 'MOVING_UP'
        ).order_by('current_floor')

        opposite_direction_elevators = opposite_direction_elevators.annotate(
            destination_floors_length=RawSQL('CARDINALITY(destination_floors)', ())
        ).filter(destination_floors_length__lt=self.elevator_system.max_queue_size)

        if opposite_direction_elevators.exists():
            return opposite_direction_elevators.first()

        return None

    def assign_floors_to_elevator(self, optimal_elevator):
        if optimal_elevator.current_floor != self.current_floor:
            destination_floors = optimal_elevator.destination_floors
            new_destination_floors = []
            inserted_current_floor = False
            inserted_destination_floor = False
            for floor in destination_floors:
                if not inserted_current_floor and self.current_floor < floor:
                    new_destination_floors.append(self.current_floor)
                    inserted_current_floor = True
                if not inserted_destination_floor and self.destination_floor < floor:
                    new_destination_floors.append(self.destination_floor)
                    inserted_destination_floor = True
                if floor != self.current_floor and floor != self.destination_floor:
                    new_destination_floors.append(floor)
            if not inserted_current_floor:
                new_destination_floors.append(self.current_floor)
            if not inserted_destination_floor:
                new_destination_floors.append(self.destination_floor)
            optimal_elevator.destination_floors = new_destination_floors
            optimal_elevator.save()






