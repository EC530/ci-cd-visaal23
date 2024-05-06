# tests/test_api.py

import pytest
from app import app as flask_app  # Import your actual Flask app
from mongomock import MongoClient
import mongomock

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongomock://localhost"
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mocker():
    """Setup Mongomock for MongoDB operations."""
    with mongomock.patch(servers=(('localhost', 27017),)):
        yield MongoClient()

def test_list_conversations(client, mocker):
    db = mocker['healthmonitoring']
    conv_col = db.conversations
    # Mock data
    conv_col.insert_one({'doctorId': 'doctor123', 'patientId': 'patient123'})
    response = client.get('/api/conversations/doctor123')
    assert response.status_code == 200
    assert type(response.json) is list

def test_get_messages(client, mocker):
    db = mocker['healthmonitoring']
    msg_col = db.messages
    # Mock data
    msg_col.insert_one({'conversationId': 'conv123', 'text': 'Hello!'})
    response = client.get('/api/conversations/conv123/messages')
    assert response.status_code == 200
    assert type(response.json) is list

def test_send_message(client, mocker):
    db = mocker['healthmonitoring']
    msg_col = db.messages
    # Send a POST request
    response = client.post('/api/conversations/conv123/send', json={'senderId': 'user123', 'text': 'Hello!'})
    assert response.status_code == 201
    assert response.json['status'] == 'Message sent'

def test_start_conversation(client, mocker):
    db = mocker['healthmonitoring']
    conv_col = db.conversations
    # Send a POST request to start a new conversation
    response = client.post('/api/conversations/start', json={'doctorId': 'doctor123', 'patientId': 'patient123'})
    assert response.status_code == 201
    assert 'conversationId' in response.json

