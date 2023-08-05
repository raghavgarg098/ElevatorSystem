from django.urls import path
from .views import ElevatorView, ElevatorSystemView, UserRequestView


urlpatterns = [
    path('elevator/<str:elevator_id>/', ElevatorView.as_view(), name='elevator'),
    path('elevator-system/', ElevatorSystemView.as_view(), name="elevator-system"),
    path('user-request/', UserRequestView.as_view(), name="user-requests"),
]


#test commit