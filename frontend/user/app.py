from flask import flash, Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap
import requests
from werkzeug.utils import secure_filename
import os
from logs_config import setup_logging
from database import db, Student, Assignment, Course, AssignmentConfig, Submission, init_db, Student_to_assignment
import docker
from datetime import datetime
from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakOpenIDConnection
from dotenv import load_dotenv

# Import the API blueprint
from api import api
load_dotenv()


# Set up logger
log_terminal = True
logger = setup_logging(log_terminal)



#Load environment variables
KEYCLOAK_SERVER_URL = os.getenv('KEYCLOAK_SERVER_URL')
KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM')
KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID')
KEYCLOAK_CLIENT_SECRET = os.getenv('KEYCLOAK_CLIENT_SECRET')
KEYCLOAK_REDIRECT_URI = os.getenv('KEYCLOAK_REDIRECT_URI')
KEYCLOAK_REALM_ADMIN = os.getenv('KEYCLOAK_REALM_ADMIN')
KEYCLOAK_ADMIN_USERNAME = os.getenv('KEYCLOAK_ADMIN_USERNAME')
KEYCLOAK_ADMIN_PASSWORD = os.getenv('KEYCLOAK_ADMIN_PASSWORD')
KEYCLOAK_SERVER_URL_POST = os.getenv('KEYCLOAK_SERVER_URL_POST')

logger.info(f"Keycloak Server URL: {KEYCLOAK_SERVER_URL}")
logger.info(f"Keycloak Realm: {KEYCLOAK_REALM}")
logger.info(f"Keycloak Client ID: {KEYCLOAK_CLIENT_ID}")
logger.info(f"Keycloak Client Secret: {KEYCLOAK_CLIENT_SECRET}")
logger.info(f"Keycloak Redirect URI: {KEYCLOAK_REDIRECT_URI}")
logger.info(f"Keycloak Admin Username: {KEYCLOAK_ADMIN_USERNAME}")
logger.info(f"Keycloak Admin Password: {KEYCLOAK_ADMIN_PASSWORD}")
logger.info(f"Keycloak Server URL POST: {KEYCLOAK_SERVER_URL_POST}")



if not all([KEYCLOAK_SERVER_URL_POST, KEYCLOAK_SERVER_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, KEYCLOAK_REDIRECT_URI]):
    raise ValueError("One or more Keycloak configuration environment variables are missing")


# Check Keycloak server accessibility
try:
    response = requests.get(KEYCLOAK_SERVER_URL_POST)
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
    #verify=False
)

app = Flask(__name__, static_folder='static', template_folder='templates')
bootstrap = Bootstrap(app)

app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # for 64 MB limit

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@postgres-application:5432/postgres'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Jacobo'  # Set a secret key for session management

# Initialize the database
init_db(app)


# Register the API blueprint
app.register_blueprint(api, url_prefix='/api')
# Fallback data
fallback_assignments = [
    {"id": 1, "title": "Lav et sort-rød træ (Det kan du ikke)", "status": 0, "requirements": "No specific requirements", "start_date":datetime.now(), "end_date":datetime.now(), "course_name": "Rizzology"},
    {"id": 2, "title": "Bevis Chernoff", "status": 1, "requirements": "Nu skal du staffes", "start_date":datetime.now(), "end_date":datetime.now(), "course_name": "Rizzology"},
    {"id": 3, "title": "Brug Bayes Theorem", "status": 3, "requirements": "No specific requirements", "start_date":datetime.now(), "end_date":datetime.now(), "course_name": "Rizzology"},
    {"id": 4, "title": "Skriv .parralel()", "status": 4, "requirements": "No specific requirements", "start_date":datetime.now(), "end_date":datetime.now(), "course_name": "Rizzology"},
    {"id": 5, "title": "Opfind Linux", "status": 2, "requirements": "No specific requirements", "start_date":datetime.now(), "end_date":datetime.now(), "course_name": "Rizzology"}
]

fallback_course = [
    {"id": 1, "name": "DM507_AlgoDat"},
    {"id": 2, "name": "DM551_AlgoSand"},
    {"id": 3, "name": "DM566_DmMl"},
    {"id": 4, "name": "DM563_CP"},
    {"id": 5, "name": "DM510_Operativsystemer"},
]

@app.route("/")
def student_dashboard():
    if 'username' not in session:
        logger.warning("Access attempt without login")
        return redirect(url_for('login', error="You need to login first"))
    
    username = session['username']
    try:
        student = Student.query.filter_by(username=username).first()
        if not student:
            raise ValueError(f"Student with username {username} not found")
        
        assignments = db.session.query(
            Assignment.id,
            Assignment.title,
            Assignment.start_date,
            Assignment.end_date,
            Course.name.label('course_name'),
            db.case(
                (Student_to_assignment.status.isnot(None), Student_to_assignment.status),
                else_=0
            ).label('status')
            ).outerjoin(Student_to_assignment, 
                        (Assignment.id == Student_to_assignment.assignment_id) & 
                        (Student_to_assignment.student_id == student.id))\
            .join(Course, Assignment.course_id == Course.id)\
            .order_by('status').all()
    except Exception as e:
        logger.error(f"Failed to retrieve assignments: {e}")
        assignments = fallback_assignments  # Use the fallback assignments if the query fails

    return render_template("student.html", nav=f"Dashboard for: {username}", assignments=assignments)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        try:
            logger.info("Establishing Keycloak connection")
            keycloak_connection = KeycloakOpenIDConnection(
                server_url=KEYCLOAK_SERVER_URL_POST,
                username=KEYCLOAK_ADMIN_USERNAME,
                password=KEYCLOAK_ADMIN_PASSWORD,
                realm_name=KEYCLOAK_REALM_ADMIN,
                client_id='',
                client_secret_key='',
                verify=True
            )
            logger.info("Keycloak connection established")
            keycloak_admin = KeycloakAdmin(connection=keycloak_connection)
            logger.info("Keycloak admin connection established")
            new_user = keycloak_admin.create_user({
                "email": email,
                "username": username,
                "enabled": True,
                "firstName": first_name,
                "lastName": last_name,
                "credentials": [{"value": password, "type": "password"}]
            }, exist_ok=False)
            logger.info(f"User {username} created successfully")
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'danger')
            logger.error(f"Failed to create account: {e}")
            return redirect(url_for('register'))

    return render_template('register.html', nav='Register')



@app.route('/landing')
def home():
    return render_template('landing_page.html', nav='Home')


@app.route('/login')
def login():
    redirect_uri = os.getenv('KEYCLOAK_REDIRECT_URI')
    auth_url = keycloak_openid.auth_url(redirect_uri=redirect_uri, scope="openid")
    return redirect(auth_url)

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
        logger.info(f"User: {userinfo['preferred_username']} logged in successfully.")
        return redirect(url_for('student_dashboard'))
    except Exception as e:
        logger.error(f"Failed to process callback: {e}")
        return 'Error: Failed to process callback.', 500


@app.route('/logout')
def logout():
    username = session.get('username', 'No User')
    session.clear()
    logger.info(f"{username} logged out.")

    # Construct the Keycloak logout URL
    keycloak_logout_url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout?redirect_uri={KEYCLOAK_REDIRECT_URI}"

    return redirect(keycloak_logout_url)


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
        assignment = next((a for a in fallback_assignments if a['id'] == assignment_id), None)
        assignment = Assignment(id=assignment['id'], title=assignment['title'], status=assignment['status'], requirements=assignment['requirements'])
        logger.info(f"Using the fallback list the user: {username} clicked assignment: {assignment}, Error: {e}")
    return render_template('submit.html', nav=f"{assignment.course}: {assignment.title}", assignment=assignment)

@app.route('/cancel_assignment/<int:assignment_id>', methods=['POST'])
def cancel_assignment(assignment_id):
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'You need to login first'}), 403
    try:
        student_id = Student.query.filter_by(username=session['username']).first().id
        assignment = Student_to_assignment.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
        submission = Submission.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
        if assignment:
            assignment.status = 0
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
            new_student_to_assignment = Student_to_assignment(assignment_id=assignment_id, student_id=student.id, status=1)
            
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

def run_docker(user_id, assignment_id, submission_id):
    logger.info(f"Running Docker for user_id: {user_id}, assignment_id: {assignment_id}, submission_id: {submission_id}")
    try:
        logger.debug(f"Fetching assignment {assignment_id} from database")
        assignment = Assignment.query.get(assignment_id)
        config = AssignmentConfig.query.filter_by(id=assignment_id).first()
        if not assignment or not config:
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
        submission.status = 3 if not stderr else 4

        # Update the Student_to_assignment status
        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        if student_to_assignment:
            student_to_assignment.status = submission.status
            logger.info(f"Updated Student_to_assignment status to {student_to_assignment.status} for user_id: {user_id}, assignment_id: {assignment_id}")

        db.session.commit()
        logger.info(f"Submission updated successfully for assignment_id: {assignment_id}, status: {submission.status}, grade: {submission.grade}")

    except docker.errors.DockerException as de:
        logger.error(f"Docker error for assignment {assignment_id}: {de}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(de)[:64]
        submission.grade = "failed"
        submission.status = 4
        db.session.commit()
        logger.warning(f"Docker error handled for assignment_id: {assignment_id}, status set to failed")

        # Update the Student_to_assignment status
        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        if student_to_assignment:
            student_to_assignment.status = submission.status
            db.session.commit()
            logger.warning(f"Updated Student_to_assignment status to {student_to_assignment.status} for user_id: {user_id}, assignment_id: {assignment_id}")

    except Exception as e:
        logger.error(f"Error running docker for assignment {assignment_id}, Error: {e}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(e)[:64]
        submission.grade = "failed"
        submission.status = 4
        db.session.commit()
        logger.warning(f"General error handled for assignment_id: {assignment_id}, status set to failed")

        # Update the Student_to_assignment status
        student_to_assignment = Student_to_assignment.query.filter_by(
            student_id=user_id,
            assignment_id=assignment_id
        ).first()
        if student_to_assignment:
            student_to_assignment.status = submission.status
            db.session.commit()
            logger.warning(f"Updated Student_to_assignment status to {student_to_assignment.status} for user_id: {user_id}, assignment_id: {assignment_id}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
