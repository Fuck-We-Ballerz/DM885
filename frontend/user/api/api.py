from flask import Blueprint, request, jsonify, session, redirect, url_for
import requests
from werkzeug.utils import secure_filename
import os
import docker
from database import db, Student, Assignment, Submission, Student_to_assignment, AssignmentConfig
from logs_config import setup_logging
from keycloak import KeycloakOpenID

# Initialize Blueprint
api = Blueprint('api', __name__)

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

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)

# Helper function to get admin token
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

@api.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']

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
        
        return jsonify({"message": "Account created successfully"}), 201
    except Exception as e:
        logger.error(f"Failed to create account: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/login')
def login():
    redirect_uri = KEYCLOAK_REDIRECT_URI
    auth_url = keycloak_openid.auth_url(redirect_uri=redirect_uri, scope="openid")
    return jsonify({"auth_url": auth_url})

@api.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        logger.info("No code provided")
        return jsonify({"error": "No code provided"}), 400
    
    try:
        token = keycloak_openid.token(
            grant_type='authorization_code',
            code=code,
            redirect_uri=KEYCLOAK_REDIRECT_URI
        )
        userinfo = keycloak_openid.userinfo(token['access_token'])
        session['username'] = userinfo['preferred_username']
        session['user'] = userinfo
        session['token'] = token  # Save the token in the session
        logger.info(f"User: {userinfo['preferred_username']} logged in successfully.")
        return redirect(url_for('api.student_dashboard'))
    except Exception as e:
        logger.error(f"Failed to process callback: {e}")
        return jsonify({"error": str(e)}), 500

@api.route("/student_dashboard")
def student_dashboard():
    if 'username' not in session:
        logger.warning("Access attempt without login")
        return jsonify({"error": "You need to login first"}), 403
    
    username = session['username']
    student_assignments = []
    
    try:
        student = Student.query.filter_by(username=username).first()
        
        if not student:
            raise ValueError(f"Student with username {username} not found")
        
        assignments = db.session.query(Assignment).all()
        
        for assignment in assignments:
            submission = Submission.query.filter_by(assignment_id=assignment.id, student_id=student.id).first()
            grade = submission.grade if submission else "Not submitted"
            student_assignments.append({
                'id': assignment.id,
                'course_name': assignment.course.name if assignment.course else 'No Course',
                'title': assignment.title,
                'start_date': assignment.start_date,
                'end_date': assignment.end_date,
                'grade': grade
            })
    except Exception as e:
        logger.error(f"Failed to retrieve assignments: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"assignments": student_assignments})

@api.route('/logout')
def logout():
    token = session.get('token', {})
    refresh_token = token.get('refresh_token')
    if refresh_token:
        try:
            requests.post(
                KEYCLOAK_LOGOUT_URL,
                data={
                    'client_id': KEYCLOAK_CLIENT_ID,
                    'client_secret': KEYCLOAK_CLIENT_SECRET,
                    'refresh_token': refresh_token
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            logger.info("Logged out of Keycloak successfully.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to log out from Keycloak: {e}")

    session.clear()
    logger.info("User session cleared.")
    return jsonify({"message": "Logged out successfully"}), 200

@api.route('/assignment/<int:assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'You need to login first'}), 403
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({'success': False, 'error': 'Assignment not found'}), 404
        assignment_data = {
            'id': assignment.id,
            'course_name': assignment.course.name if assignment.course else 'No Course',
            'title': assignment.title,
            'start_date': assignment.start_date,
            'end_date': assignment.end_date
        }
        return jsonify({'success': True, 'assignment': assignment_data}), 200
    except Exception as e:
        logger.error(f"Failed to retrieve assignment {assignment_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api.route('/upload', methods=['POST'])
def upload_file():
    assignment_id = session.get('assignment_id')
    username = session.get('username')
    
    if 'file' not in request.files:
        logger.debug(f"{username} tried to upload a file, No file to upload")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.debug(f"{username} tried to upload a file, but the filename is empty")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join('/user/upload', username)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        logger.info(f"{username} successfully uploaded file: {filename}")
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            student = Student.query.filter_by(username=username).first()
            new_submission = Submission(assignment_id=assignment_id, student_id=student.id, submission=data)
            new_student_to_assignment = Student_to_assignment(assignment_id=assignment_id, student_id=student.id)
            
            db.session.add(new_submission)
            db.session.add(new_student_to_assignment)
            db.session.commit()
            logger.info(f"Submission created for assignment: {assignment_id} by student: {username}")
            logger.info(f"Student_to_assignment created for assignment: {assignment_id} by student: {username} with status 1")
            
            run_docker(student.id, assignment_id, new_submission.id)
            return jsonify({"message": f"You successfully uploaded: {filename}"}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to create submission for assignment: {assignment_id}, Error {e}")
            return jsonify({'error': str(e)}), 500
    else:
        logger.debug(f"{username} tried to upload a file of invalid file type: {filename}")
        return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

def run_docker(user_id, assignment_id, submission_id):
    logger.info(f"Running Docker for user_id: {user_id}, assignment_id: {assignment_id}, submission_id: {submission_id}")
    try:
        assignment = Assignment.query.get(assignment_id)
        config = AssignmentConfig.query.filter_by(id=assignment.config_id).first()
        if not assignment or not config:
            raise ValueError("Invalid assignment or configuration")
        logger.info(f"Assignment and configuration found for assignment_id: {assignment_id}")

        image = "alpine"
        submission = Submission.query.get(submission_id)

        client = docker.from_env()
        logger.debug("Docker client initialized")

        mem_limit = max(int(config.max_ram), 6 * 1024 * 1024)
        cpu_count = int(config.max_cpu)
        logger.info(f"Running container with mem_limit: {mem_limit}, cpu_count: {cpu_count}")

        container = client.containers.run(
            image,
            command="echo 'Hello World'",
            detach=True,
            mem_limit=mem_limit,
            cpu_count=cpu_count,
        )
        logger.info(f"Container started for assignment_id: {assignment_id}")

        container.wait()
        logger.info(f"Container execution completed for assignment_id: {assignment_id}")

        stdout = container.logs(stdout=True, stderr=False)
        stderr = container.logs(stdout=False, stderr=True)

        submission.submission_std = stdout.decode('utf-8') if stdout else ''
        submission_err = stderr.decode('utf-8') if stderr else ''
        submission.submission_err = submission_err[:64]
        submission.grade = "passed" if not stderr else "failed"

        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        db.session.commit()
        logger.info(f"Submission updated successfully for assignment_id: {assignment_id}, grade: {submission.grade}")

    except docker.errors.DockerException as de:
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(de)[:64]
        submission.grade = "failed"
        db.session.commit()

        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        db.session.commit()

    except Exception as e:
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(e)[:64]
        submission.grade = "failed"
        db.session.commit()

        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        db.session.commit()
