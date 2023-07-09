from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.db import transaction
from ..models import ElevatorSystem, Elevator


class ElevatorSystemView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate the input parameters
        number_of_elevators = request.data.get('number_of_elevators')
        max_queue_size = request.data.get('max_queue_size')

        try:
            number_of_elevators = int(number_of_elevators)
            max_queue_size = int(max_queue_size)
            if number_of_elevators <= 0 or max_queue_size <= 0:
                raise ValidationError("Number of elevators and max queue size must be positive integers.")
        except (TypeError, ValueError):
            raise ValidationError("Number of elevators and max queue size must be integers.")

        # Create an elevator system entity
        elevator_system = ElevatorSystem.objects.create(
            elevators_number=number_of_elevators,
            max_queue_size=max_queue_size
        )

        # Create elevator rows with foreign key as elevator system id
        elevators = []
        for _ in range(number_of_elevators):
            elevator = Elevator(
                elevator_system=elevator_system,
                status='AVAILABLE',
                door_status='CLOSE',
                current_floor=0,
                destination_floors=[]
            )
            elevators.append(elevator)

        # Bulk create the elevators in a transaction
        with transaction.atomic():
            Elevator.objects.bulk_create(elevators)

        # Get the elevator IDs
        elevator_ids = [elevator.id for elevator in elevators]

        # Return the elevator system ID and elevator IDs in the response
        response_data = {
            'elevator_system_id': elevator_system.id,
            'elevator_ids': elevator_ids
        }

        # Return the response as JSON
        return JsonResponse(response_data)
