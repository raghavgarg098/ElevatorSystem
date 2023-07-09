from django.http import JsonResponse
from rest_framework.views import APIView
from ..models import Elevator, UserRequest
from ..managers import ElevatorManager


class ElevatorView(APIView):
    def get(self, request, elevator_id, *args, **kwargs):
        # Get the requested actions from the query parameters
        requests = request.GET.get('requests')
        next_destination = request.GET.get('next_destination')
        status = request.GET.get('status')

        # Get the Elevator instance based on the elevator_id
        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return JsonResponse({'error': 'Elevator not found'}, status=404)

        response_data = {}

        # Handle the requests action
        if requests:
            requests_list = UserRequest.objects.filter(
                elevator_id=elevator_id,
                status__in=['INITIALIZED', 'PROCESSING']
            ).values('id', 'current_floor', 'destination_floor', 'status')
            response_data['requests'] = list(requests_list)

        # Handle the next_destination action
        if next_destination:
            if elevator.destination_floors:
                next_destination_floor = elevator.destination_floors[0]
                response_data['next_destination'] = next_destination_floor

        # Handle the status action
        if status:
            response_data['status'] = elevator.status
            response_data['door_status'] = elevator.door_status

        # Return the response data as JSON
        return JsonResponse(response_data)

    def patch(self, request, elevator_id, *args, **kwargs):
        action = request.data.get('action')

        try:
            elevator = Elevator.objects.get(id=elevator_id)
        except Elevator.DoesNotExist:
            return JsonResponse({'error': 'Elevator not found'}, status=404)

        em = ElevatorManager(elevator_id, elevator=elevator)

        if em.can_execute_action(action):
            return em.execute_action(action)
        else:
            return JsonResponse({'error': 'Action Not Found'}, status=400)






