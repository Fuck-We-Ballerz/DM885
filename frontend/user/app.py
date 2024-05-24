from flask import flash, Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap
import requests
from werkzeug.utils import secure_filename
import os
from logs_config import setup_logging
from database import db, Student, Assignment, Course, AssignmentConfig, Submission, init_db, Student_to_assignment
import docker
from datetime import datetime
import time
from keycloak import KeycloakOpenID
#from dotenv import load_dotenv

#load_dotenv()

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
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

KEYCLOAK_TOKEN_URL = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
KEYCLOAK_USER_CREATION_URL = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users"

#Debugging
logger.info(f"Keycloak Server URL: {KEYCLOAK_SERVER_URL}")
logger.info(f"Keycloak Realm: {KEYCLOAK_REALM}")
logger.info(f"Keycloak Client ID: {KEYCLOAK_CLIENT_ID}")
logger.info(f"Keycloak Client Secret: {KEYCLOAK_CLIENT_SECRET}")
logger.info(f"Keycloak Redirect URI: {KEYCLOAK_REDIRECT_URI}")
logger.info(f"Keycloak Admin Username: {KEYCLOAK_ADMIN_USERNAME}")
logger.info(f"Keycloak Admin Password: {KEYCLOAK_ADMIN_PASSWORD}")

# If one of the Keycloak environment variables is missing, raise an error
if not all([KEYCLOAK_SERVER_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, KEYCLOAK_REDIRECT_URI]):
    raise ValueError("One or more Keycloak configuration environment variables are missing")

# Retry connecting to Keycloak server
for _ in range(1000):
    try:
        response = requests.get(KEYCLOAK_SERVER_URL)
        response.raise_for_status()
        logger.info("Keycloak server is accessible")
        break
    except requests.RequestException as e:
        logger.error(f"Failed to reach Keycloak server: {e}")
        time.sleep(10)
else:
    raise RuntimeError("Failed to connect to Keycloak server after multiple attempts")

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
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres-application:5432/{POSTGRES_DB}'
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

# This is the dashboard for the student
@app.route("/")
def student_dashboard():
    if 'username' not in session:
        logger.warning("Access attempt without login")
        return redirect(url_for('login', error="You need to login first"))
    
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
                'id': assignment.id,  # Ensure 'id' is included
                'course_name': assignment.course.name if assignment.course else 'No Course',
                'title': assignment.title,
                'start_date': assignment.start_date,
                'end_date': assignment.end_date,
                'grade': grade
            })
    except Exception as e:
        logger.error(f"Failed to retrieve assignments: {e}")
        student_assignments = []

    return render_template("student.html", nav=f"Dashboard for: {username}", assignments=student_assignments)


# The register route allows students to create an account through Keycloak, this entry is also put in the database
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

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
            
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'danger')
            logger.error(f"Failed to create account: {e}")
            return redirect(url_for('register'))

    return render_template('register.html', nav='Register')

# The landing page, login or register
@app.route('/landing')
def home():
    return render_template('landing_page.html', nav='Home')

# The login route redirects to Keycloak for authentication
@app.route('/login')
def login():
    redirect_uri = os.getenv('KEYCLOAK_REDIRECT_URI')
    auth_url = keycloak_openid.auth_url(redirect_uri=redirect_uri, scope="openid")
    return redirect(auth_url)

# The callback route processes the response from Keycloak, and saves the user information in the session, which is later used to log out
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        logger.info("No code provided")
        return 'Error: No code provided.', 400
    
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
        return redirect(url_for('student_dashboard'))
    except Exception as e:
        logger.error(f"Failed to process callback: {e}")
        return 'Error: Failed to process callback.', 500


# Logout of the application, and also from Keycloak
@app.route('/logout')
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
    return redirect(BASE_URL)

# The route to view a specific assignment
@app.route('/submit/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = session.get('username', 'No user')
    session['assignment_id'] = assignment_id
    print("Info for /student", username, assignment_id)
    try:
        print("User getting assignment from database")
        assignment = Assignment.query.get(session.get('assignment_id'))
        logger.info(f"User clicked assignment: {assignment}")
    except Exception as e:
        logger.info(f" Error: {e}")
    return render_template('submit.html', nav=f"{assignment.course}: {assignment.title}", assignment=assignment)

# Cancel the assignment
@app.route('/cancel_assignment/<int:assignment_id>', methods=['POST'])
def cancel_assignment(assignment_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'You need to login first'}), 403
    try:
        student_id = Student.query.filter_by(username=session['username']).first().id
        assignment = Student_to_assignment.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
        submission = Submission.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
        if assignment:
            db.session.delete(submission)
            db.session.delete(assignment)
            db.session.commit()
            logger.info(f"Assignment {assignment_id} status set to 0 by user {session['username']}")
            return jsonify({'success': True}), 200
        else:
            logger.warning(f"Assignment {assignment_id} not found")
            return jsonify({'success': False, 'error': 'Assignment not found'}), 404
    except Exception as e:
        logger.error(f"Failed to cancel assignment {assignment_id}: {e}")
        return jsonify({'success': False, 'error': 'Failed to cancel assignment'}), 500

# The route to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    assignment_id = session.get('assignment_id', 'No Assignment')
    logger.info(f"Uploading for assignment: {assignment_id}")
    
    upload_folder = '/user/upload'
    username = session.get('username', 'No User')
    assignment_id = session.get('assignment_id', 'No Assignment')
    
    if not os.path.exists(upload_folder):
        try:
            os.makedirs(upload_folder, exist_ok=True)
            logger.info(f"Folder: {upload_folder} created")
        except Exception as e:
            logger.debug(f"Failed to create the folder: {upload_folder}, Error {e}")
    
    if 'file' not in request.files:
        logger.debug(f"{username} tried to upload a file, No file to upload")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        logger.debug(f"{username} tried to upload a file, but the filename is empty")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
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
        except Exception as e:
            print("Error in submission", e)
            db.session.rollback()
            logger.error(f"Failed to create submission for assignment: {assignment_id}, Error {e}")
        
        return redirect(url_for('student_dashboard', nav="Student", error=f"You successfully uploaded: {filename}")) 
    else:
        logger.debug(f"{username} tried to upload a file of invalid file type: {filename}")
        return jsonify({'error': 'Invalid file type'}), 400

# Check if the file is a zip file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

# Run the submission in a Docker container
def run_docker(user_id, assignment_id, submission_id):
    logger.info(f"Running Docker for user_id: {user_id}, assignment_id: {assignment_id}, submission_id: {submission_id}")
    try:
        logger.debug(f"Fetching assignment {assignment_id} from database")
        assignment = Assignment.query.get(assignment_id)
        config = AssignmentConfig.query.filter_by(id=assignment.config_id).first()
        if not assignment or not config:
            logger.error(f'Invalid assignment or configuration for assignment_id: {assignment_id} and config_id: {config.id}')
            raise ValueError("Invalid assignment or configuration")
        logger.info(f"Assignment and configuration found for assignment_id: {assignment_id}")

        image = "alpine"
        logger.debug(f"Fetching submission {submission_id} from database")
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

        logger.debug("Fetching submission to update")
        submission.submission_std = stdout.decode('utf-8') if stdout else ''
        submission_err = stderr.decode('utf-8') if stderr else ''
        submission.submission_err = submission_err[:64]
        submission.grade = "passed" if not stderr else "failed"

        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        if student_to_assignment:
            logger.info(f"Updated Student_to_assignment status to for user_id: {user_id}, assignment_id: {assignment_id}")

        db.session.commit()
        logger.info(f"Submission updated successfully for assignment_id: {assignment_id}, grade: {submission.grade}")

    except docker.errors.DockerException as de:
        logger.error(f"Docker error for assignment {assignment_id}: {de}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(de)[:64]
        submission.grade = "failed"
        db.session.commit()
        logger.warning(f"Docker error handled for assignment_id: {assignment_id}, status set to failed")

        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        if student_to_assignment:
            db.session.commit()
            logger.warning(f"Updated Student_to_assignment status to for user_id: {user_id}, assignment_id: {assignment_id}")

    except Exception as e:
        logger.error(f"Error running docker for assignment {assignment_id}, Error: {e}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(e)[:64]
        submission.grade = "failed"
        db.session.commit()
        logger.warning(f"General error handled for assignment_id: {assignment_id}, status set to failed")

        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        if student_to_assignment:
            db.session.commit()
            logger.warning(f"Updated Student_to_assignment status to for user_id: {user_id}, assignment_id: {assignment_id}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
