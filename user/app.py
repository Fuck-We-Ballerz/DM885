from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap  # Import Flask-Bootstrap
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import *
from logs_config import setup_logging
import requests
from datetime import datetime
from sqlalchemy.dialects.postgresql import BYTEA

# Set up logger
# set log_temrinal to True, if you want logs in the terminal, otherwise set to False
log_terminal = True 
logger = setup_logging(log_terminal)

app = Flask(__name__)
bootstrap = Bootstrap(app)  # Initialize Flask-Bootstrap
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # for 64 MB limit

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgres_application/testdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
app.secret_key = 'Jacobo'  # Set a secret key for session management

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    docker_image = db.Column(db.Text)
    config_id = db.Column(db.Integer, db.ForeignKey('assignment_config.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    status = db.Column(db.Integer, default=0)
    requirements = db.Column(db.String(1000), default="No specific requirements")
    # Relationship to Course
    course = db.relationship('Course', backref=db.backref('assignments', lazy=True))
    
    
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    
    
class AssignmentConfig(db.Model):
    __tablename__ = 'assignment_config'
    id = db.Column(db.Integer, primary_key=True)
    max_ram = db.Column(db.Integer, nullable=False)
    max_cpu = db.Column(db.Float, nullable=False)
    max_time = db.Column(db.Interval, nullable=False)
    max_submission = db.Column(db.Integer, nullable=False)
    # Relationship to Assignment
    assignments = db.relationship('Assignment', backref='config', lazy=True)


class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(64), default='Not graded', nullable=False)
    status = db.Column(db.String(64), default='Pending', nullable=False)
    submission = db.Column(BYTEA)  # For storing binary data, such as a zip file
    submission_std = db.Column(db.String(64), default='', nullable=False)
    submission_err = db.Column(db.String(64), default='', nullable=False)
    submission_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    # Relationships
    assignment = db.relationship('Assignment', backref=db.backref('submissions', lazy=True))
    student = db.relationship('Student', backref=db.backref('submissions', lazy=True))


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
        assignments = Assignment.query.order_by(Assignment.status).join(Course).all()  # Ensure each assignment has the course loaded
    except Exception as e:
        logger.error(f"Failed to retrieve assignments: {e}")
        

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
    try:
        assignment = Assignment.query.get(assignment_id)
        logger.info(f"User clicked assignment: {assignment}")
    except:
        # Use a fallback if the database query fails
        assignment = next((a for a in fallback_assignments if a['id'] == assignment_id), None)
        assignment = Assignment(id=assignment['id'], title=assignment['title'], status=assignment['status'], requirements=assignment['requirements'])
        logger.info(f"Using the fallback list the user: {username} clicked assignment: {assignment}")
    return render_template('submit.html', nav=f"{assignment.course}: {assignment.title}", assignment=assignment)


@app.route('/student/upload', methods=['POST'])
def upload_file():
    assignemt_id = session.get('assignment_id', 'No Assignment')
    logger.info(f"Uploading for assignment: {assignemt_id}")
    
    upload_folder= '/user/upload'
    username = session.get('username', 'No User')
    assignemt_id = session.get('assignment_id', 'No Assignment')
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
        file.save(os.path.join(upload_folder, filename))
        logger.info(f"{username} succesfully uploaded file: {filename}")
        # sql update Assignement
        try:
            assignment = Assignment.query.get(assignemt_id)
            logger.info(f"Assignment: {assignemt_id} status: {assignment.status}")
            assignment.status = 1
            db.session.commit()
            logger.info(f"Assignment: {assignemt_id} updated to status {assignment.status}")
        except Exception as e:
            logger.error(f"Failed to update assignment: {assignemt_id}, Error {e}")
        
        # sql create submission
        try:
            with(open(os.path.join(upload_folder, filename), 'rb')) as f:
                data = f.read()
                
            student = Student.query.filter_by(username=username).first()
            new_submission = Submission(assignment_id=assignemt_id, student_id=student.id, submission=data)
            db.session.add(new_submission)
            db.session.commit()
            logger.info(f"Submission created for assignment: {assignemt_id} by student: {username}")
        except Exception as e:
            db.session.rollback()
            
            logger.error(f"Failed to create submission for assignment: {assignemt_id}, Error {e}")
        
        return redirect(url_for('student', nav="Student", error=f"You Succesfully uploaded: {filename}")) 
    else:
        logger.debug(f"{username} tried to upload a file of invalid file type: {filename}")
        return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050)
