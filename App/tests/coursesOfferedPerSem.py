import pytest, unittest
from App.models import CoursesOfferedPerSem
from App.controllers import addSemesterCourses, create_course, isCourseOffered, get_all_OfferedCodes, delete_all_records
from App.main import create_app
from App.database import db, create_db


class CoursesOfferedPerSemUnitTests(unittest.TestCase):

    def test_new_offered_course(self):
        course_code = "INFO2605"
        offered_course = CoursesOfferedPerSem(course_code)
        self.assertEqual(offered_course.code, course_code)
    
    def test_offered_course_toJSON(self):
        course_code = "INFO2605"
        offered_course = CoursesOfferedPerSem(course_code)
        offered_course_json = offered_course.get_json()
        self.assertDictEqual(offered_course_json, {"ID:": None, "Course Code:": course_code})

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class CoursesOfferedPerSemIntegrationTests(unittest.TestCase):
    def test_add_offered_course(self):
        prereqs=[]
        course_code = "INFO2605"
        create_course(course_code, "Professional Ethics and Law", 3, 4, prereqs)
        addSemesterCourses(course_code)
        self.assertTrue(isCourseOffered(course_code))

    def test_get_all_offered_courses_json(self):
        create_course("MATH2250", "Industrial Statistics",4,3,[])
        create_course("INFO2605", "Professional Ethics and Law", 3, 4, [])
        addSemesterCourses("MATH2250")
        addSemesterCourses("INFO2605")
        offered_courses = get_all_OfferedCodes()

        assert "MATH2250" in offered_courses
        assert "INFO2605" in offered_courses

    def test_remove_all_offered(self):
        
        create_course("MATH2250", "Industrial Statistics", 4, 3, [])
        create_course("INFO2605", "Professional Ethics and Law", 3, 4, [])
        addSemesterCourses("MATH2250")
        addSemesterCourses("INFO2605")

        # Check that courses are offered
        assert isCourseOffered("MATH2250")
        assert isCourseOffered("INFO2605")

        # Remove all offered courses
        delete_all_records()

        # Check that courses are no longer offered
        assert not isCourseOffered("MATH2250")
        assert not isCourseOffered("INFO2605")






