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
    create_course,
    enroll_in_programme,
    get_all_students_json,
    update_student,
    getCompletedCourses,
)


LOGGER = logging.getLogger(__name__)


class StudentUnitTest(unittest.TestCase):

    def test_new_student(self):
        student = Student("01234", "johnpass", "John Doe", 1)
        assert student.name == "John Doe"

    def test_student_toJSON(self):
        student = Student("01234", "johnpass", "John Doe", 1)
        student_json = student.get_json()
        self.assertDictEqual(
            {"name": "John Doe", "student_id": "01234", "program": 1}, student_json)


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
            "01234", "johnpass", "John Doe", program.name)
        assert student.name == "John Doe"

    def test_get_all_student_json(self):
        program = create_program("Computer Science Major", 3, 4, 5)
        create_student("01234", "johnpass", "John Doe", program.name)
        users_json = get_all_students_json()
        self.assertListEqual(
            [{"name": "John Doe", "student_id": "01234", "program": 1}], users_json)

    def test_update_student(self):
        program = create_program("Computer Science Major", 3, 4, 5)
        create_student("01234", "johnpass", "John Doe", program.name)
        student = update_student("01234", "Bill")
        assert student.name == "Bill"

    # def test_add_course_to_plan(self):
    #     course_code = "INFO2605"
    #     prereqs = []
    #     create_course("INFO2605", "Professional Ethics and Law", 3, 4, prereqs)
    #     addSemesterCourses(course_code)
    #     program = create_program("Computer Science Major", 3, 4, 5)
    #     student = create_student(
    #         "01234", "johnpass", "John Doe", program.name)
    #     self.assertTrue(addCourseToPlan(student, course_code))

    # def test_remove_course_from_plan(self):
    #     course_code = "INFO2605"
    #     prereqs = []
    #     create_course("INFO2605", "Professional Ethics and Law", 3, 4, prereqs)
    #     addSemesterCourses(course_code)
    #     program = create_program("Computer Science Major", 3, 4, 5)
    #     student = create_student(
    #         "01234", "johnpass", "John Doe", program.name)
    #     plan = create_CoursePlan(1)
    #     addSemesterCourses(course_code)
    #     addCourseToPlan(student, course_code)
    #     enroll_in_programme(student.id, 1)
    #     removeCourse(student, course_code)
    #     course_from_course_plan = getCourseFromCoursePlan(plan.planId, course_code)
    #     self.assertEqual(course_from_course_plan.planId, 1)
    #     self.assertEqual(course_from_course_plan.code, "INFO2605")

    def test_enroll_in_programme(self):
        program = create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "01234", "johnpass", "John Doe", program.name)
        enroll_in_programme(student.id, 1)
        assert enroll_in_programme(student.id, 1) == 1

    # def test_view_course_plan(self):
    #     course_code = "MATH2250"
    #     create_course(
    #         "/Users/jervalthomas/Desktop/Programming /Year 4 Sem 1/COMP 3613/flaskmvc/testData/courseData.csv")
    #     addSemesterCourses(course_code)
    #     program = create_program("Computer Science Major", 3, 4, 5)
    #     student = create_student(
    #         "816025522", "Password", "Jerval", program.name)
    #     create_CoursePlan(1)
    #     addSemesterCourses(course_code)
    #     addCourseToPlan(student, course_code)
    #     enroll_in_programme(student.id, 1)
    #     plan_json = view_course_plan(student)
    #     self.assertListEqual(
    #         [{"name": "Jerval", "student_id": "816025522", "program": 1}], plan_json)