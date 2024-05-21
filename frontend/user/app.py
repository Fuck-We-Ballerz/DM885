from flask import flash, Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
from logs_config import setup_logging
from database import db, Student, Assignment, Course, AssignmentConfig, Submission, init_db, Student_to_assignment
import docker
from datetime import datetime

# Import the API blueprint
from api import api

# Set up logger
log_terminal = True
logger = setup_logging(log_terminal)

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
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            new_student = Student(username=username, password=password, name=username)
            try:
                db.session.add(new_student)
                db.session.commit()
                flash("Account created successfully", "success")
                logger.info(f"User: {username} successfully registered.")
                return redirect(url_for('login', nav="Login", success="Account created successfully"))
            except Exception as e:
                flash("Registration failed", "error")
                logger.error(f"Failed to register user: {username}, Error: {e}")
                return redirect(url_for('register', nav="Register", error="Registration failed"))
        else:
            flash("Registration failed, due to empty input", "error")
            logger.warning("Empty registration submission")
            return redirect(url_for('register', nav="Register", error="Input cannot be empty"))
    else:
        return render_template('register.html', nav="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    logger.info(url_for('login'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            try:
                student = Student.query.filter_by(username=username).first()
                logger.info(f'User: {username} trying to log in')
                logger.info(f"Student: {student.username} found with password: {student.password}")
                if student and student.password == password:
                    session['username'] = student.username 
                    logger.info(f"Student: {student.username} logged in successfully.")
                    return redirect(url_for('student_dashboard'))
                else:
                    if username == "admin" and password == "admin":
                        session['username'] = username
                        logger.info("Bypass database using admin")
                        return redirect(url_for('student_dashboard'))
                    logger.debug(f"User: {username} failed to log in.")
                    return redirect(url_for('login', nav="Login", error="Invalid username or password"))
            except Exception as e:
                if username == "admin" and password == "admin":
                    session['username'] = username
                    logger.info("Bypass database using admin")
                    return redirect(url_for('student_dashboard'))
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
    username = session.get('username', 'No User')
    session.clear()
    logger.info(f"{username} logged out.")
    return redirect(url_for('login'))

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
