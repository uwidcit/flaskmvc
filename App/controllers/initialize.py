from .user import create_student, create_employer, create_staff
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_student('student', 'studentpass', 'UWI', 'Computer Science', 3.5)
    create_employer('employer', 'employerpass')
    create_staff('staff', 'staffpass')
