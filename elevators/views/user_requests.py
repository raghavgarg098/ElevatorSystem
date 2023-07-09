from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from ..managers import UserRequestManager


class UserRequestView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate the input parameters
        current_floor = request.data.get('current_floor')
        destination_floor = request.data.get('destination_floor')
        elevator_system_id = request.data.get('elevator_system_id')

        try:
            current_floor = int(current_floor)
            destination_floor = int(destination_floor)
        except (TypeError, ValueError):
            raise ValidationError("Current floor and destination floor must be integers.")

        urm = UserRequestManager(current_floor, destination_floor, elevator_system_id)
        return urm.assign_user_request()
