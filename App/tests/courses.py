import pytest, unittest
from App.models import Course

class CourseUnitTests(unittest.TestCase):

    def test_new_course(self):
        course = Course()
        self.assertIsInstance(course, Course)

    def test_course_json(self):
        course = Course()
        course_json = course.get_json()
        self.assertDictEqual(course_json, {
            'Course Code:': None,
            'Course Name: ': None,
            'Course Rating: ': None,
            'No. of Credits: ': None,
            'Prerequistes: ': []})
    
    # def test_get_course_credits(self):

   