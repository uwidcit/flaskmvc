from App.models import Student
from App.database import db

def enroll_in_programme(self, username, password, student_id, name, programme):
    student = Student(username, password, student_id, name)
    programme.add_student(student)
    self.students.append(student)

def add_course_to_plan(self, student_id, course):
    student = self.get_student_by_id(student_id)
    if student:
        student.add_course_to_plan(course)

def remove_course_from_plan(self, student_id, course):
    student = self.get_student_by_id(student_id)
    if student:
        student.remove_course_from_plan(course)

def view_course_plan(self, student_id):
    student = self.get_student_by_id(student_id)
    if student:
        return student.view_course_plan()

def add_course(self, student_id, courses, file):
    student = self.get_student_by_id(student_id)
    if student:
        student.add_course(courses, file)

def get_student_by_id(self, student_id):
    for student in self.students:
        if student.id == student_id:
            return student
    return None