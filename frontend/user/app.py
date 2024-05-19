from ast import Sub
from re import sub
from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap  # Import Flask-Bootstrap
from werkzeug.utils import secure_filename
import os
from logs_config import setup_logging
import requests
from datetime import datetime
from sqlalchemy.dialects.postgresql import BYTEA
from database import db, Student, Assignment, Course, AssignmentConfig, Submission, init_db, Student_to_assignment
import docker

# Set up logger
# set log_terminal to True, if you want logs in the terminal, otherwise set to False
log_terminal = True
logger = setup_logging(log_terminal)

app = Flask(__name__)
bootstrap = Bootstrap(app)  # Initialize Flask-Bootstrap
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # for 64 MB limit

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgres-application/postgres'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'Jacobo'  # Set a secret key for session management
# Initialize the database
init_db(app)

# In case we are not connected to the database, we can use this as fallback
fallback_assignments = [
    {"id": 1, "title": "Lav et sort-rød træ (Det kan du ikke)", "status": 0, "requirements": "No specific requirements"},
    {"id": 2, "title": "Bevis Chernoff", "status": 1, "requirements": "Nu skal du staffes"},
    {"id": 3, "title": "Brug Bayes Theorem", "status": 3, "requirements": "No specific requirements"},
    {"id": 4, "title": "Skriv .parralel()", "status": 4, "requirements": "No specific requirements"},
    {"id": 5, "title": "Opfind Linux", "status": 2, "requirements": "No specific requirements"}
]

fallback_course = [
    {"id": 1, "name": "DM507_AlgoDat"},
    {"id": 2, "name": "DM551_AlgoSand"},
    {"id": 3, "name": "DM566_DmMl"},
    {"id": 4, "name": "DM563_CP"},
    {"id": 5, "name": "DM510_Operativsystemer"},
]


@app.route("/")
def homepage():
    logger.debug("Redirecting from homepage to login")
    return redirect(url_for('login', error="You must login first"))

@app.route("/student")
def student():
    if 'username' not in session:
        logger.warning("Access attempt without login")
        return redirect(url_for('login', error="You need to login first"))

    username = session['username']
    try:
        # Get the student's assignments with status
        student = Student.query.filter_by(username=username).first()
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

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password: # Check if the inputs are not empty
          
            #headers = {'content-type': 'application/x-www-form-urlencoded',}
            
            # Define data for HTTP request
            
            data = {
                'username': username,
                'password': password,
                'grant_type': 'password',
                'client_id': 'student_service',
                'client_secret': 'K0hdiACFA0sJOmgDc3xyMbwuhUh7fWpp'
            }
            try:
                response = requests.post('http://localhost:3200/auth/realms/DM855/protocol/openid-connect/token', headers=headers, data=data)
                if response.status_code == 200:
                    session['username'] = username
                    return redirect(url_for('student'))
                else:
                    return redirect(url_for('login', nav="Login", error="Invalid username or password"))
            except Exception as e:
                    logger.error(f"HTTP request failed: {e}")
                    return redirect(url_for('login', nav="Login", error="Invalid username or password"))    
            
        else:
            logger.warning("Empty login submission")
            return redirect(url_for('login', nav="Login", error="Input cannot be empty"))
    else:
        return render_template('login.html', nav="Login")
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password: # Check if the inputs are not empty
            try:
                student = Student.query.filter_by(username=username).first()
                # Check if the student exists and the username and the password is correct
                if student and username == student.username and password == student.password: # Check if the username and password are correct
                    session['username'] = student.username 
                    logger.info(f"User: {username} has succesfully logged in.")
                    return redirect(url_for('student'))
                else:
                    logger.debug(f"User: {username} failed to log in.")
                    return redirect(url_for('login', nav="Login", error="Invalid username or password"))
            
            # In case the database is not connected. Used for testing without db
            except Exception as e:
                if username == "admin" and password == "admin":
                    session['username'] = username
                    logger.info(f"Bypass database using admin") 
                    return redirect(url_for('student'))
                else:
                    logger.error(f"Database not connected: {e}")
                    return redirect(url_for('login', nav="Login", error="Invalid username or password"))
                    
        else:
            logger.warning("Empty login submission")
            return redirect(url_for('login', nav="Login", error="Input cannot be empty"))
    else:
        return render_template('login.html', nav="Login")

@app.route('/logout')
def logout():
    # Clear the session
    username = session.get('username', 'No User')
    session.clear()
    # Redirect to the login page
    logger.info(f"{username} logged out.")
    return redirect(url_for('login'))

@app.route('/student/submit/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    username = session.get('username', 'No user')
    session['assignment_id'] = assignment_id
    print("Info for /student", username, assignment_id)
    try:
        print("User getting assignment from database")
        assignment = Assignment.query.get(session.get('assignment_id'))
        logger.info(f"User clicked assignment: {assignment}")
    except Exception as e:
        # Use a fallback if the database query fails
        assignment = next((a for a in fallback_assignments if a['id'] == assignment_id), None)
        assignment = Assignment(id=assignment['id'], title=assignment['title'], status=assignment['status'], requirements=assignment['requirements'])
        logger.info(f"Using the fallback list the user: {username} clicked assignment: {assignment}, Error: {e}")
    return render_template('submit.html', nav=f"{assignment.course}: {assignment.title}", assignment=assignment)


@app.route('/student/cancel_assignment/<int:assignment_id>', methods=['POST'])
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



@app.route('/student/upload', methods=['POST'])
def upload_file():
    assignment_id = session.get('assignment_id', 'No Assignment')
    logger.info(f"Uploading for assignment: {assignment_id}")
    
    upload_folder= '/user/upload'
    username = session.get('username', 'No User')
    assignment_id = session.get('assignment_id', 'No Assignment')
    
    # Check if directory exists, and if not, create it
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
        logger.info(f"{username} succesfully uploaded file: {filename}")
        
        # SQL create submission
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
            
            # Run Docker container with the uploaded file
            run_docker(student.id, assignment_id, new_submission.id, file_path)
        except Exception as e:
            print("Error in submission", e)
            db.session.rollback()
            logger.error(f"Failed to create submission for assignment: {assignment_id}, Error {e}")
        
        return redirect(url_for('student', nav="Student", error=f"You Succesfully uploaded: {filename}")) 
    else:
        logger.debug(f"{username} tried to upload a file of invalid file type: {filename}")
        return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

def run_docker(user_id, assignment_id, submission_id, file_path):
    try:
        # Get information from the database
        assignment = Assignment.query.get(assignment_id)
        config = AssignmentConfig.query.filter_by(id=assignment_id).first()
        if not assignment or not config:
            raise ValueError("Invalid assignment or configuration")

        image = assignment.docker_image if assignment.docker_image else "python:3.12-slim"
        submission_id = Submission.query.get(submission_id).id

        # Docker client setup
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')

        # Bind the directory containing the zip file
        host_directory = os.path.dirname(file_path)
        container_directory = "/app"
        file_name = os.path.basename(file_path)

        # Ensure memory limit is at least 6MB
        mem_limit = max(int(config.max_ram), 6 * 1024 * 1024)
        cpu_count = int(config.max_cpu)

        container = client.containers.run(
            image,
            command=f"sh -c 'unzip /app/{file_name} -d /app && python3 /app/test.py'",
            detach=True,
            mem_limit=mem_limit,
            cpu_count=cpu_count,
            volumes={host_directory: {'bind': container_directory, 'mode': 'rw'}}
        )

        # Wait for the container to finish
        container.wait()

        # Fetch logs
        stdout = container.logs(stdout=True, stderr=False)
        stderr = container.logs(stdout=False, stderr=True)

        # Update the submission with the output
        submission = Submission.query.get(submission_id)
        submission.submission_std = stdout.decode('utf-8') if stdout else ''
        submission_err = stderr.decode('utf-8') if stderr else ''
        submission.submission_err = submission_err[:64]  # Truncate to 64 characters
        submission.grade = "passed" if not stderr else "failed"
        submission.status = 3 if not stderr else 4

        db.session.commit()

    except docker.errors.DockerException as de:
        logger.error(f"Docker error for assignment {assignment_id}: {de}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(de)[:64]  # Truncate to 64 characters
        submission.grade = "failed"
        submission.status = 4
        db.session.commit()
    except Exception as e:
        logger.error(f"Error running docker for assignment {assignment_id}, Error: {e}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(e)[:64]  # Truncate to 64 characters
        submission.grade = "failed"
        submission.status = 4
        db.session.commit()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050)
