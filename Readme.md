# **Elevator System Project**

This project aims to simulate an elevator system that manages elevators and user requests within a building.

## **Models**

### Elevator System

The ElevatorSystem model represents the overall elevator system within a building. It has the following fields:

##### name:

A string field representing the name of the elevator system.

##### max_queue_size: 

An integer field indicating the maximum number of floors that can be queued in an elevator's destination floors list.


### Elevator

The Elevator model represents an individual elevator within the elevator system. It has the following fields:

##### elevator_system: 

A foreign key to the ElevatorSystem model

##### status: 
A choice field indicating the status of the elevator (e.g., moving up, moving down, available).

##### door_status: 
A choice field indicating the status of the elevator door (e.g., open, closed).

##### current_floor: 
An integer field representing the current floor where the elevator is located.

##### destination_floors: 
An array field containing the list of destination floors queued for the elevator.

### User Request

The UserRequest model represents a user's request for an elevator. It has the following fields:

##### current_floor: 
An integer field representing the floor where the user is currently located.

##### destination_floor: 
An integer field representing the desired destination floor for the user.

##### status: 
A choice field indicating the status of the user request (e.g., initialized, processing, processed).

##### elevator:
A foreign key to the Elevator model, indicating the assigned elevator for the user request.

## APIs and Actions

The following APIs are available for interacting with the elevator system:

### Elevator API

#### GET /api/elevator/{elevator_id}: 
Retrieves the list of elevators. Parameters can be provided to get specific information such as requests, next destination, or status.

#### PATCH /api/elevator/{elevator_id}/: 

Performs an action on the specified elevator. The action can be one of the following: MOVE, OPEN_DOOR, CLOSE_DOOR, MARK_AVAILABLE, MARK_UNAVAILABLE, or REACH_DESTINATION.

#### POST REQUEST API  /api/user-request/

Creates a new user request. The request should include the current floor, destination floor, and elevator system ID. The API will assign the request to an appropriate elevator based on the system's logic.

#### POST ELEVATOR SYSTEM API  /api/elevator-system/

Creates an elevator system with given lifts and maximum queue size a lift can maintain


Please note that the above API endpoints are just examples, and you may need to adjust them based on your specific implementation and URL configurations.

Getting Started
To set up and run the Elevator System project, follow these steps:

Clone the project repository to your local machine.
Install the necessary dependencies and libraries in requirements.txt in your virtual env
Set up the database and run the migrations.
Start the development server.
Access the project APIs using the provided endpoints and perform actions on the elevators and user requests.