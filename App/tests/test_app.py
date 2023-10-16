import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Program
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    update_user,
    create_student,
    addCoursetoHistory,
    create_program,
    addCourseToPlan,
    create_course,
    hasCourseInPlan,
    )


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

class StudentIntegrationTests(unittest.TestCase):

    def setUp(self):
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        self.app = app.test_client()

        with app.app_context():
            create_db()
            db.create_all()

    def tearDown(self):
        with self.app:
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_create_student(self):
            program = create_program("Computer Science Major", 3,4,5)
            student = create_student("816025522", "Password", "Jerval", program.name)
            assert student.name == "Jerval"

    def test_add_course_to_plan(self):
            create_course("/Users/jervalthomas/Desktop/Programming /Year 4 Sem 1/COMP 3613/flaskmvc/testData/courseData.csv")
            program = create_program("Computer Science Major", 3,4,5)
            student = create_student("816025522", "Password", "Jerval", program.name)
            course_code = "MATH2250"
            addCourseToPlan(student, course_code)
            self.assertTrue(hasCourseInPlan(course_code))

    def test_remove_course_from_plan(self):
            student = create_student("816025522", "Password", "Jerval", "Computer Science")
            course_code = "COMP101"
            addCourseToPlan(student, course_code)
            self.assertTrue(hasCourseInPlan(course_code))
            student.removeCourseFromPlan(course_code)
            self.assertFalse(hasCourseInPlan(course_code))

    def test_enroll_in_programme(self):
            student = create_student("816025522", "Password", "Jerval", "Computer Science")
            program_name = "Computer Science Program"
            student.enroll_in_programme(program_name)
            self.assertEqual(student.program.name, program_name)
