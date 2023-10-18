import os
import tempfile
import pytest
import logging
import unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Program, StudentCourseHistory
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
    addSemesterCourses,
    getCourseFromCoursePlan,
    removeCourse,
    enroll_in_programme,
    get_all_students_json,
    update_student,
    get_student_by_id,
    getCompletedCourses,
    create_CoursePlan,
    view_course_plan
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
        self.assertDictEqual(user_json, {"id": None, "username": "bob"})

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
    app = create_app(
        {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
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
        self.assertListEqual([{"id": 1, "username": "bob"}, {
                             "id": 2, "username": "rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


class StudentUnitTest(unittest.TestCase):
    def setUp(self):
        app = create_app(
            {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
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
        program = create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "816025522", "Password", "Jerval", program.name)
        assert student.name == "Jerval"

    def test_get_all_student_json(self):
        program = create_program("Computer Science Major", 3, 4, 5)
        create_student("816025522", "Password", "Jerval", program.name)
        users_json = get_all_students_json()
        self.assertListEqual(
            [{"name": "Jerval", "student_id": "816025522", "program": 1}], users_json)

    def test_update_student(self):
        program = create_program("Computer Science Major", 3, 4, 5)
        create_student("816025522", "Password", "Jerval", program.name)
        student = update_student("816025522", "Bill")
        assert student.name == "Bill"


class StudentIntegrationTests(unittest.TestCase):

    def setUp(self):
        app = create_app(
            {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
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
        program = create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "816025522", "Password", "Jerval", program.name)
        assert student.name == "Jerval"

    def test_add_course_to_plan(self):
        course_code = "MATH2250"
        create_course(
            "/Users/jervalthomas/Desktop/Programming /Year 4 Sem 1/COMP 3613/flaskmvc/testData/courseData.csv")
        addSemesterCourses(course_code)
        program = create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "816025522", "Password", "Jerval", program.name)
        self.assertTrue(addCourseToPlan(student, course_code))

    def test_remove_course_from_plan(self):
        course_code = "MATH2250"
        create_course(
            "/Users/jervalthomas/Desktop/Programming /Year 4 Sem 1/COMP 3613/flaskmvc/testData/courseData.csv")
        addSemesterCourses(course_code)
        program = create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "816025522", "Password", "Jerval", program.name)
        plan = create_CoursePlan(1)
        addSemesterCourses(course_code)
        addCourseToPlan(student, course_code)
        enroll_in_programme(student.id, 1)
        removeCourse(student, course_code)
        course_from_course_plan = getCourseFromCoursePlan(plan.planId, course_code)
        self.assertEqual(course_from_course_plan.planId, 1)
        self.assertEqual(course_from_course_plan.code, "MATH2250")
        

    def test_enroll_in_programme(self):
        create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "816025522", "Password", "Jerval", "Computer Science Major")
        enroll_in_programme(student.id, 1)
        assert enroll_in_programme(student.id, 1) == 1

    def test_view_course_plan(self):
        course_code = "MATH2250"
        create_course(
            "/Users/jervalthomas/Desktop/Programming /Year 4 Sem 1/COMP 3613/flaskmvc/testData/courseData.csv")
        addSemesterCourses(course_code)
        program = create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "816025522", "Password", "Jerval", program.name)
        create_CoursePlan(1)
        addSemesterCourses(course_code)
        addCourseToPlan(student, course_code)
        enroll_in_programme(student.id, 1)
        plan_json = view_course_plan(student)
        self.assertListEqual(
            [{"name": "Jerval", "student_id": "816025522", "program": 1}], plan_json)


class CourseHistoryUnitTest(unittest.TestCase):

    def setUp(self):
        app = create_app(
            {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        self.app = app.test_client()

        with app.app_context():
            create_db()
            db.create_all()

    def tearDown(self):
        with self.app:
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_create_course_history(self):
        student_course_history = StudentCourseHistory(123, 'MATH1115')

        # Assert that the attributes are set correctly
        self.assertEqual(student_course_history.studentID, 123)
        self.assertEqual(student_course_history.code, 'MATH1115')

    def test_get_json(self):
        create_program("Computer Science Major", 3, 4, 5)
        create_course(
        "/Users/jervalthomas/Desktop/Programming /Year 4 Sem 1/COMP 3613/flaskmvc/testData/courseData.csv")
        student = create_student("816025522", "Password",
                             "Jerval", "Computer Science Major")
        student_course_history = StudentCourseHistory(123, 'MATH1115')
        addCoursetoHistory(student.id, "MATH1115")

        result = student_course_history.get_json()

        expected_result = {"Program ID": None, "Course Code": "MATH1115"}

        self.assertDictEqual(expected_result, result)


class CourseHistoryIntegrationTests(unittest.TestCase):

    def setUp(self):
        app = create_app(
            {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        self.app = app.test_client()

        with app.app_context():
            create_db()
            db.create_all()

    def tearDown(self):
        with self.app:
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_add_Course_to_History(self):
        create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "816025522", "Password", "Jerval", "Computer Science Major")
        create_course(
            "/Users/jervalthomas/Desktop/Programming /Year 4 Sem 1/COMP 3613/flaskmvc/testData/courseData.csv")
        addCoursetoHistory(student.id, "INFO1601")
        completed_courses = getCompletedCourses(student.id)
        assert len(completed_courses) == 1
        for course_history in completed_courses:
            self.assertIsInstance(course_history, StudentCourseHistory)
            self.assertEqual(course_history.studentID, student.id)
