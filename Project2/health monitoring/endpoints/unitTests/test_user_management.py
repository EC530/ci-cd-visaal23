# tests/test_app.py

import pytest
from flask import Flask
from flask_pymongo import PyMongo
from app import app as flask_app  # Make sure to import your actual Flask app
from mongomock import MongoClient

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config['TESTING'] = True
    flask_app.config["MONGO_URI"] = "mongomock://localhost"
    db = MongoClient()
    flask_app.db = db
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_add_user(client):
    """Test adding a new user."""
    response = client.post('/admin/users', json={
        'username': 'johndoe',
        'roles': ['admin']
    })
    assert response.status_code == 201
    assert 'user_id' in response.get_json()

def test_list_users(client):
    """Test listing users."""
    response = client.get('/admin/users')
    assert response.status_code == 200

def test_update_user(client):
    """Test updating a user."""
    response = client.put('/admin/users/12345', json={
        'personalInfo': {'firstName': 'John', 'lastName': 'Doe'},
        'roles': ['user']
    })
    assert response.status_code == 404  # Assuming user doesn't exist for test

def test_delete_user(client):
    """Test deleting a user."""
    response = client.delete('/admin/users/12345')
    assert response.status_code == 404  # Assuming user doesn't exist for test

def test_assign_roles(client):
    """Test assigning roles to a user."""
    response = client.post('/admin/users/12345/roles', json={'roles': ['admin']})
    assert response.status_code == 404  # Assuming user doesn't exist for test

def test_remove_role(client):
    """Test removing roles from a user."""
    response = client.delete('/admin/users/12345/roles', json={'roles': ['admin']})
    assert response.status_code == 404  # Assuming user doesn't exist for test

def test_search_user_details(client):
    """Test searching for user details."""
    response = client.get('/admin/search/details', query_string={'name': 'John Doe'})
    assert response.status_code == 404  # Assuming user doesn't exist for test
