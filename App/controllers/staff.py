from program import Program
from course import Course
from App.models import Staff

class StaffController:
    def __init__(self):
        self.programmes = []  # Store programme instances here
        self.courses = []     # Store course instances here

    def add_programme(self, programme_name, description):
        programme = Programme(programme_name, description)
        self.programmes.append(programme)

    def remove_programme(self, programme_name):
        programme = self.get_programme_by_name(programme_name)
        if programme:
            self.programmes.remove(programme)

    def add_course(self, course_code, course_name, credits):
        course = Course(course_code, course_name, credits)
        self.courses.append(course)

    def remove_course(self, course_code):
        course = self.get_course_by_code(course_code)
        if course:
            self.courses.remove(course)

    def get_programme_by_name(self, programme_name):
        for programme in self.programmes:
            if programme.name == programme_name:
                return programme
        return None

    def get_course_by_code(self, course_code):
        for course in self.courses:
            if course.code == course_code:
                return course
        return None
