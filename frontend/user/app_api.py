from flask import Flask, request, jsonify, session, redirect, url_for, flash, render_template
from flask_bootstrap import Bootstrap
import requests
from werkzeug.utils import secure_filename
import os
from logs_config import setup_logging
from database import db, Student, Assignment, Course, AssignmentConfig, Submission, init_db, Student_to_assignment
import docker
from datetime import datetime
from keycloak import KeycloakOpenID
from dotenv import load_dotenv

load_dotenv()

# Set up logger
log_terminal = True
logger = setup_logging(log_terminal)

# Load environment variables
KEYCLOAK_SERVER_URL = os.getenv('KEYCLOAK_SERVER_URL')
KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM')
KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')
KEYCLOAK_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET')
KEYCLOAK_REDIRECT_URI = os.getenv('KEYCLOAK_REDIRECT_URI')
KEYCLOAK_ADMIN_USERNAME = os.getenv('KEYCLOAK_ADMIN_USERNAME')
KEYCLOAK_ADMIN_PASSWORD = os.getenv('KEYCLOAK_ADMIN_PASSWORD')
BASE_URL = os.getenv('BASE_URL')
KEYCLOAK_LOGOUT_URL = os.getenv('KEYCLOAK_LOGOUT_URL')

KEYCLOAK_TOKEN_URL = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
KEYCLOAK_USER_CREATION_URL = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users"

# If one of the Keycloak environment variables is missing, raise an error
if not all([KEYCLOAK_SERVER_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, KEYCLOAK_REDIRECT_URI]):
    raise ValueError("One or more Keycloak configuration environment variables are missing")

# Check Keycloak server accessibility
try:
    response = requests.get(KEYCLOAK_SERVER_URL)
    logger.info(f"RESPONSE: {response.status_code}")
    response.raise_for_status()
    logger.info("Keycloak server is accessible")
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to reach Keycloak server: {e}")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)

# Initialize the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
bootstrap = Bootstrap(app)

# Set the maximum file size for uploads and the database URI, along with the secret key
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # for 64 MB limit
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@postgres-application:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')  # Set a secret key for session management

# Initialize the database
init_db(app)

# Get the admin token for Keycloak, in order to create students
def get_admin_token():
    payload = {
        'client_id': KEYCLOAK_CLIENT_ID,
        'client_secret': KEYCLOAK_CLIENT_SECRET,
        'grant_type': 'password',
        'username': KEYCLOAK_ADMIN_USERNAME,
        'password': KEYCLOAK_ADMIN_PASSWORD
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(KEYCLOAK_TOKEN_URL, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()['access_token']

@app.route('/api/create_user', methods=['POST'])
def api_create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    if not all([username, password, first_name, last_name, email]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        token = get_admin_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {token}"
        }
        user_data = {
            "username": username,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "enabled": True,
            "credentials": [{
                "type": "password",
                "value": password,
                "temporary": False
            }]
        }
        response = requests.post(KEYCLOAK_USER_CREATION_URL, json=user_data, headers=headers)
        response.raise_for_status()
        logger.info(f"User {username} created successfully")

        # Create a new student in the database
        new_student = Student(username=username, name=first_name, password="")
        db.session.add(new_student)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        logger.error(f"Failed to create account: {e}")
        return jsonify({'error': f'Failed to create account: {str(e)}'}), 500

# Other routes...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
