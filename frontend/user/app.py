from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap  # Import Flask-Bootstrap
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import *

app = Flask(__name__)
bootstrap = Bootstrap(app)  # Initialize Flask-Bootstrap
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # for 64 MB limit

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@postgres-application/postgres'

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
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Integer, default=0)
    requirements = db.Column(db.String(1000), default="No specific requirements")

# In case we are not connected to the database, we can use this as fallback
fallback_assignments = [
    {"id": 1, "name": "DM507_AlgoDat", "status": 0, "requirements": "No specific requirements"},
    {"id": 2, "name": "DM551_AlgoSand", "status": 1, "requirements": "Nu skal du staffes"},
    {"id": 3, "name": "DM566_DmMl", "status": 3, "requirements": "No specific requirements"},
    {"id": 4, "name": "DM563_CP", "status": 4, "requirements": "No specific requirements"},
    {"id": 5, "name": "DM510_Operativsystemer", "status": 2, "requirements": "No specific requirements"}
]


@app.route("/")
def homepage():
    return redirect(url_for('login', error="You must login first"))

@app.route("/student")
def student():
    if 'username' not in session:
        return redirect(url_for('login', error="You need to login first"))

    username = session['username']
    try:
        assignments = Assignment.query.order_by(Assignment.status).all()
    except:
        # If there's an error (e.g., database is not reachable), use fallback assignments
        assignments = [Assignment(id=a['id'], name=a['name'], status=a['status']) for a in fallback_assignments]

    return render_template("student.html", nav=f"Dashboard for: {username}", assignments=assignments)


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
                    return redirect(url_for('student'))
                else:
                    return render_template('login.html', nav="Login", error="Invalid username or password")
            
            # In case the database is not connected. Used for testing without db
            except:
                if username == "admin" and password == "admin":
                    session['username'] = username 
                    return redirect(url_for('student'))
                else:
                    return render_template('login.html', nav="Login", error="Invalid username or password")
                    
        else:
            return render_template('login.html', nav="Login", error="Input cannot be empty")
    else:
        return render_template('login.html', nav="Login")

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the login page
    return redirect(url_for('login'))


@app.route('/student/submit', methods=['GET', 'POST'])
def submit():
    username = session.get('username', 'No User')
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:
            # Save the file to the server's filesystem or handle it as needed
            filename = secure_filename(file.filename)
            file.save(os.path.join('/path_to_save_files', filename))
            return 'File successfully uploaded'
    return render_template('submit.html', nav=f"Submit for: {username}")


@app.route('/student/submit/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    try:
        assignment = Assignment.query.get(assignment_id)
    except:
        # Use a fallback if the database query fails
        assignment = next((a for a in fallback_assignments if a['id'] == assignment_id), None)
        assignment = Assignment(id=assignment['id'], name=assignment['name'], status=assignment['status'], requirements=assignment['requirements'])

    return render_template('submit.html', nav=f"Submit Assignment: {assignment.name}", assignment=assignment)


@app.route('/student/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('/user/upload', filename))
        return jsonify({'message': 'File successfully uploaded'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050)
