from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap  # Import Flask-Bootstrap
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)  # Initialize Flask-Bootstrap
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # for 64 MB limit
app.secret_key = 'Jacobo'  # Set a secret key for session management


assignments = [("Assignment 1", 0), ("Assignment 2", 1), ("Assignment 3", 3), ("Assignment 4", 4), ("Assignment 5", 2)]
@app.route("/student")
def index():
    # Ensure assignments is defined (even if empty) before sorting and passing to the template
    username = session.get('username', 'No User')  
    
    if assignments is None:
        sorted_assignments = []
    else:
        sorted_assignments = sorted(assignments, key=lambda x: x[1])

    return render_template("index.html", nav= f"Dashbord for: {username}", assignments=sorted_assignments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "admin":
            session['username'] = username 
            return redirect(url_for('index'))
        else:
            return render_template('login.html', nav="Login", error="Invalid username or password")
    else:
        return render_template('login.html', nav="Login")


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
    app.run(debug=True, port=8080)
