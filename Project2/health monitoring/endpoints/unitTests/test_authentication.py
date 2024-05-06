# tests/test_auth.py

import pytest
from app import create_app
from bson.objectid import ObjectId
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({"TESTING": True, "MONGO_URI": "mongodb://localhost:27017/myTestDB"})
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

# Test registration endpoint
def test_register(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'roles': ['user'],
        'firstName': 'Test',
        'lastName': 'User',
        'dateOfBirth': '1990-01-01'
    })
    assert response.status_code == 201
    assert 'user_id' in response.get_json()

# Test login endpoint
def test_login(client):
    # Pre-insert a user for login testing
    password_hash = generate_password_hash('mypassword')
    # Here you would normally interact with the database to insert the test user
    # For example:
    # mongo.db.authentication.insert_one({...})

    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'mypassword'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Login successful'

# Test logout endpoint
def test_logout(client):
    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Logged out successfully'
