from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
import os
from logs_config import setup_logging
from database import db, Student, Assignment, Submission, Student_to_assignment, AssignmentConfig, Course
from werkzeug.security import generate_password_hash, check_password_hash
import docker

fallback_assignments = [
    {"id": 1, "title": "Lav et sort-rød træ (Det kan du ikke)", "status": 0, "requirements": "No specific requirements"},
    {"id": 2, "title": "Bevis Chernoff", "status": 1, "requirements": "Nu skal du staffes"},
    {"id": 3, "title": "Brug Bayes Theorem", "status": 3, "requirements": "No specific requirements"},
    {"id": 4, "title": "Skriv .parralel()", "status": 4, "requirements": "No specific requirements"},
    {"id": 5, "title": "Opfind Linux", "status": 2, "requirements": "No specific requirements"}
]

# Set up logger
log_terminal = True
logger = setup_logging(log_terminal)

api = Blueprint('api', __name__)

@api.route("/register", methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_student = Student(username=username, password=hashed_password)
        try:
            db.session.add(new_student)
            db.session.commit()
            logger.info(f"User: {username} successfully registered.")
            return jsonify({"message": "Account created successfully"}), 201
        except Exception as e:
            logger.error(f"Failed to register user: {username}, Error: {e}")
            return jsonify({"error": "Registration failed"}), 500
    else:
        logger.warning("Empty registration submission")
        return jsonify({"error": "Input cannot be empty"}), 400

@api.route("/login", methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        try:
            student = Student.query.filter_by(username=username).first()
            if student and check_password_hash(student.password, password):
                session['username'] = student.username 
                logger.info(f"User: {username} has successfully logged in.")
                return jsonify({"message": "Login successful"}), 200
            else:
                logger.debug(f"User: {username} failed to log in.")
                return jsonify({"error": "Invalid username or password"}), 401
        except Exception as e:
            logger.error(f"Database not connected: {e}")
            return jsonify({"error": "Database error"}), 500
    else:
        logger.warning("Empty login submission")
        return jsonify({"error": "Input cannot be empty"}), 400

@api.route("/logout", methods=['POST'])
def api_logout():
    username = session.get('username', 'No User')
    session.clear()
    logger.info(f"{username} logged out.")
    return jsonify({"message": "Logged out successfully"}), 200

@api.route("/assignments", methods=['GET'])
def api_get_assignments():
    if 'username' not in session:
        logger.warning("Access attempt without login")
        return jsonify({"error": "You need to login first"}), 403
    
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
        assignments_list = [assignment._asdict() for assignment in assignments]
        return jsonify(assignments_list), 200
    except Exception as e:
        logger.error(f"Failed to retrieve assignments: {e}")
        return jsonify(fallback_assignments), 500

@api.route('/submit/<int:assignment_id>', methods=['POST'])
def api_submit_assignment(assignment_id):
    if 'username' not in session:
        return jsonify({'error': 'You need to login first'}), 403
    
    username = session['username']
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return jsonify({'error': 'Assignment not found'}), 404

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = '/user/upload'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            student = Student.query.filter_by(username=username).first()
            new_submission = Submission(assignment_id=assignment_id, student_id=student.id, submission=file.read())
            new_student_to_assignment = Student_to_assignment(assignment_id=assignment_id, student_id=student.id, status=1)
            
            db.session.add(new_submission)
            db.session.add(new_student_to_assignment)
            db.session.commit()

            run_docker(student.id, assignment_id, new_submission.id, file_path)
            return jsonify({"message": "File uploaded and processed successfully"}), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to submit assignment: {assignment_id}, Error: {e}")
        return jsonify({'error': 'Submission failed'}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

def run_docker(user_id, assignment_id, submission_id, file_path):
    try:
        assignment = Assignment.query.get(assignment_id)
        config = AssignmentConfig.query.filter_by(id=assignment_id).first()
        if not assignment or not config:
            raise ValueError("Invalid assignment or configuration")

        image = assignment.docker_image if assignment.docker_image else "python:3.12-slim"
        submission_id = Submission.query.get(submission_id).id

        client = docker.DockerClient(base_url='unix://var/run/docker.sock')

        host_directory = os.path.dirname(file_path)
        container_directory = "/app"
        file_name = os.path.basename(file_path)

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

        container.wait()

        stdout = container.logs(stdout=True, stderr=False)
        stderr = container.logs(stdout=False, stderr=True)

        submission = Submission.query.get(submission_id)
        submission.submission_std = stdout.decode('utf-8') if stdout else ''
        submission_err = stderr.decode('utf-8') if stderr else ''
        submission.submission_err = submission_err[:64]  
        submission.grade = "passed" if not stderr else "failed"
        submission.status = 3 if not stderr else 4

        db.session.commit()

    except docker.errors.DockerException as de:
        logger.error(f"Docker error for assignment {assignment_id}: {de}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(de)[:64]  
        submission.grade = "failed"
        submission.status = 4
        db.session.commit()
    except Exception as e:
        logger.error(f"Error running docker for assignment {assignment_id}, Error: {e}")
        submission = Submission.query.get(submission_id)
        submission.submission_err = str(e)[:64]  
        submission.grade = "failed"
        submission.status = 4
        db.session.commit()
