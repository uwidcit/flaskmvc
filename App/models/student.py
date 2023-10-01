from user import User  # Import the User class from user.py
from App.database import db

class Student(User):
    id = db.Column(db.String(10), foreign_key=True, unique=True)
    name = db.Column(db.String(50))

    # Define a one-to-many relationship with PassCourses
    course_history = db.relationship('PassCourses', backref='student', lazy=True)

    # Define a many-to-many relationship with CoursePlan
    courses = db.relationship('CoursePlan', secondary='student_course', back_populates='students')

    # Define a many-to-many relationship with Programme
    programmes = db.relationship('Programme', secondary='student_programme', back_populates='students')

    def __init__(self, username, password, student_id, name):
        super().__init__(username, password)
        self.id = student_id
        self.name = name

    def get_json(self):
        user_json = super().get_json()
        user_json['student_id'] = self.id
        user_json['name'] = self.name
        return user_json

    # You can add more methods specific to the Student class here

# Define the many-to-many association table for courses
student_course_association = db.Table('student_course',
    db.Column('student_id', db.String(10), db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course_plan.id'))
)

# Define the many-to-many association table for programmes
student_programme_association = db.Table('student_programme',
    db.Column('student_id', db.String(10), db.ForeignKey('student.id')),
    db.Column('programme_id', db.Integer, db.ForeignKey('programme.id'))
)
