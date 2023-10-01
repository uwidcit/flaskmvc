from App.models import CoursePlan, Program, PassCourses
from App.database import db


def enroll_in_programme(self, programme_id):
        programme = Program.query.get(programme_id)
        if programme:
            self.student.programmes.append(programme)
            db.session.commit()

def add_course_to_plan(self, course_id):
        course = CoursePlan.query.get(course_id)
        if course:
            self.student.courses.append(course)
            db.session.commit()

def remove_course_from_plan(self, course_id):
        course = CoursePlan.query.get(course_id)
        if course:
            self.student.courses.remove(course)
            db.session.commit()

def view_course_plan(self):
        return [course.get_json() for course in self.student.courses]

def add_courses_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                course_ids = [line.strip() for line in file.readlines()]
                for course_id in course_ids:
                    self.add_course_to_plan(course_id)
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return str(e)