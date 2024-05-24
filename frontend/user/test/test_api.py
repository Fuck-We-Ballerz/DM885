import os
import tempfile
import pytest
import uuid
from app import app
from database import db, init_db, Student

@pytest.fixture
def client():
    # Create a temporary database for testing
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            init_db(app)
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_register(client):
    unique_username = f"testuser_{uuid.uuid4()}"
    response = client.post('/api/register', json={
        'username': unique_username,
        'password': 'testpass',
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'{unique_username}@example.com'
    })
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['message'] == 'Account created successfully'

def test_login(client):
    response = client.get('/api/login')
    json_data = response.get_json()
    assert response.status_code == 200
    assert 'auth_url' in json_data

def test_student_dashboard(client):
    unique_username = f"testuser_{uuid.uuid4()}"
    client.post('/api/register', json={
        'username': unique_username,
        'password': 'testpass',
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'{unique_username}@example.com'
    })
    with client.session_transaction() as sess:
        sess['username'] = unique_username
    
    response = client.get('/api/student_dashboard')
    json_data = response.get_json()
    assert response.status_code == 200
    assert 'assignments' in json_data

# Additional tests can be written in a similar fashion for other endpoints
