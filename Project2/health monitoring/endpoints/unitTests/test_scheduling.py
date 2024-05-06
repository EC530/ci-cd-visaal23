# tests/test_appointments.py

import pytest
from app import create_app
from bson.objectid import ObjectId
from datetime import datetime

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Example of a test for creating an appointment
def test_create_appointment(client):
    response = client.post('/appointments', json={
        'patientId': '1',
        'doctorId': '1',
        'date': '2023-05-10',
        'time': '14:00',
        'location': 'Clinic A',
        'priority': 'High'
    })
    assert response.status_code == 201
    assert 'appointmentId' in response.get_json()

# Example of a test for fetching appointments
def test_get_appointments(client):
    response = client.get('/appointments')
    assert response.status_code == 200

# Example of a test for updating an appointment
def test_update_appointment(client):
    # Assuming you have an appointment ID to work with
    appointment_id = 'some_existing_appointment_id'  # replace this with a valid ID during testing
    response = client.put(f'/appointments/{appointment_id}', json={
        'newDate': '2023-05-11',
        'newTime': '16:00'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Appointment rescheduled successfully'

# Example of a test for deleting an appointment
def test_delete_appointment(client):
    appointment_id = 'some_existing_appointment_id'  # replace this with a valid ID during testing
    response = client.delete(f'/appointments/{appointment_id}')
    assert response.status_code == 204

