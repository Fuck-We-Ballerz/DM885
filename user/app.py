from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap  # Import Flask-Bootstrap
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import *

app = Flask(__name__)
bootstrap = Bootstrap(app)  # Initialize Flask-Bootstrap
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # for 64 MB limit

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/testdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
app.secret_key = 'Jacobo'  # Set a secret key for session management

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    


assignments = [("Assignment 1", 0), ("Assignment 2", 1), ("Assignment 3", 3), ("Assignment 4", 4), ("Assignment 5", 2)]

@app.route("/")
def homepage():
    return redirect(url_for('login', error="You must login first"))

@app.route("/student")
def student():
    if session:
        # Ensure assignments is defined (even if empty) before sorting and passing to the template
        username = session.get('username', 'No User')  
        
        if assignments is None:
            sorted_assignments = []
        else:
            sorted_assignments = sorted(assignments, key=lambda x: x[1])

        return render_template("student.html", nav= f"Dashbord for: {username}", assignments=sorted_assignments)
    else:
        return redirect(url_for('login', error="You need to login first"))


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

@app.route('/student/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('/user/uploaded', filename))
        return jsonify({'message': 'File successfully uploaded'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5050)
