from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
class Staff(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  
  programmes = db.relationship('Programme', backref='staff')
  
  def add_programme(self, programme):
    self.programmes.append(programme)

  def remove_programme(self, programme):  
    self.programmes.remove(programme)
    
  def __repr__(self):
    return f'<Staff {self.name}>'

    
class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  
  programme_id = db.Column(db.Integer, db.ForeignKey('programme.id'))
  programme = db.relationship('Programme', backref='students')
  
  courseplan = db.relationship('CoursePlan', backref='student', uselist=False)
  
  def enroll_in_programme(self, programme):
    self.programme = programme
    
  def add_course_to_plan(self, course):
    self.courseplan.courses.append(course)
    
  def remove_course_from_plan(self, course):
    self.courseplan.courses.remove(course)
    
  def __repr__(self):
    return f'<Student {self.name}>'

