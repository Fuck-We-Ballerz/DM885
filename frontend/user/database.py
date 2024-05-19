from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database
db = SQLAlchemy()

# Model definitions
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
    requirements = db.Column(db.String(1000), default="No specific requirements")
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
    assignments = db.relationship('Assignment', backref='config', lazy=True)

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(64), default='Not graded', nullable=False)
    status = db.Column(db.String(64), default='Pending', nullable=False)
    submission = db.Column(db.LargeBinary)  # For storing binary data, such as a zip file
    submission_std = db.Column(db.String(64), default='', nullable=False)
    submission_err = db.Column(db.String(64), default='', nullable=False)
    submission_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    assignment = db.relationship('Assignment', backref=db.backref('submissions', lazy=True))
    student = db.relationship('Student', backref=db.backref('submissions', lazy=True))
    
class Student_to_assignment(db.Model):
    __tablename__ = 'student_to_assignment'
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    status = db.Column(db.Integer, default=0, nullable=False)
    


def init_db(app):
    db.init_app(app)
