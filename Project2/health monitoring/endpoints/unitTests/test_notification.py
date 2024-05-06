# tests/test_app.py

import pytest
from app import app as flask_app  # Adjust the import according to your project structure
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mongo():
    """Setup Mongomock for MongoDB operations."""
    client = MongoClient()
    yield client.medicalDatabase

@pytest.fixture
def redis():
    """Setup fakeredis for Redis operations."""
    return FakeStrictRedis()

@pytest.fixture
def rq_queue(redis):
    """Setup a fake RQ queue."""
    return Queue(connection=redis)

@pytest.fixture
def rq_scheduler(rq_queue):
    """Setup a fake RQ scheduler."""
    return Scheduler(queue=rq_queue, connection=rq_queue.connection)

def test_get_patients_with_devices(mongo):
    # Setup data
    mongo.patients.insert_one({"name": "John Doe", "devices": [{"type": "heart monitor"}]})
    from app import get_patients_with_devices
    patients = get_patients_with_devices()
    assert len(patients) == 1
    assert patients[0]['name'] == 'John Doe'

def test_has_updated_reading_today(mongo):
    # Setup data
    today = datetime.now().strftime("%Y-%m-%d")
    mongo.patients.insert_one({"name": "John Doe", "devices": [{"dailyReadings": [{"date": today}]}]})
    from app import has_updated_reading_today
    patient = mongo.patients.find_one()
    assert has_updated_reading_today(patient) == True

def test_notify_patient_and_doctor(monkeypatch):
    test_notifications = []
    def mock_notify(patient):
        test_notifications.append(patient["name"])
    monkeypatch.setattr('app.notify_patient_and_doctor', mock_notify)
    from app import notify_patient_and_doctor
    notify_patient_and_doctor({"name": "John Doe"})
    assert test_notifications == ["John Doe"]

def test_schedule_daily_checks(rq_scheduler, monkeypatch):
    def mock_schedule(scheduled_time, func, interval):
        assert scheduled_time is not None
        assert func.__name__ == "check_and_notify"
        assert interval == 86400
    monkeypatch.setattr(rq_scheduler, 'schedule', mock_schedule)
    from app import schedule_daily_checks
    schedule_daily_checks()

def test_start_checks(client, monkeypatch):
    def mock_schedule_daily_checks():
        return "Scheduled daily checks"
    monkeypatch.setattr('app.schedule_daily_checks', mock_schedule_daily_checks)
    response = client.get('/start_checks')
    assert response.data.decode() == "Scheduled daily checks"
    assert response.status_code == 200
