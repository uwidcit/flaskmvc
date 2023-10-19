import pytest, unittest
from App.models import Course
from App.controllers import create_course, courses_Sorted_byRating_Objects, get_course_by_courseCode
from App.main import create_app
from App.database import db, create_db

class CourseUnitTests(unittest.TestCase):

    def test_new_course(self):
        courseCode = "INFO2605"
        courseName = "Professional Ethics and Law"
        credits = 3
        rating = 4 

        course = Course(courseCode, courseName, rating, credits)

        self.assertEqual(course.courseCode, courseCode)
        self.assertEqual(course.courseName, courseName)
        self.assertEqual(course.credits, credits)
        self.assertEqual(course.rating, rating)

    def test_course_json(self):
        courseCode = "INFO2605"
        courseName = "Professional Ethics and Law"
        credits = 3
        rating = 4 
        
        course = Course(courseCode, courseName, rating, credits)
        course_json = course.get_json()

        self.assertDictEqual(course_json, {
            'Course Code:': courseCode,
            'Course Name: ': courseName,
            'Course Rating: ': rating,
            'No. of Credits: ': credits
            })
    
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

def test_create_course():
    courseCode = "INFO2605"
    courseName = "Professional Ethics and Law"
    credits = 3
    rating = 4 
    prereqs=[]

    course = create_course(courseCode, courseName, rating, credits, prereqs)

    assert get_course_by_courseCode("INFO2605") != None


class CourseIntegrationTests(unittest.TestCase):    
    def test_courses_sorted_by_rating(self):
        prereqs=[]

        create_course("COMP6000", "DNS", 3, 3, prereqs)
        create_course("COMP6001", "DSN", 1, 3, prereqs)
        sortedCourses = courses_Sorted_byRating_Objects()

        self.assertTrue(sortedCourses)

        for i in range(len(sortedCourses) - 1):
            self.assertLessEqual(sortedCourses[i].rating, sortedCourses[i + 1].rating)
