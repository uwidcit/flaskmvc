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

class CourseHistoryUnitTest(unittest.TestCase):

    def test_create_course_history(self):
        student_course_history = StudentCourseHistory(123, "INFO2605")
        self.assertEqual(student_course_history.studentID, 123)
        self.assertEqual(student_course_history.code, "INFO2605")

    def test_course_history_toJSON(self):
        student_course_history = StudentCourseHistory(123, 'MATH1115')
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
        program = create_program("Computer Science Major", 3, 4, 5)
        student = create_student(
            "01234", "johnpass", "John Doe", program.name)
        prereqs = []
        create_course("INFO2605", "Professional Ethics and Law", 3, 4, prereqs)
        addCoursetoHistory(student.id, "INFO2605")
        completed_courses = getCompletedCourses(student.id)
        assert len(completed_courses) == 1
        for course_history in completed_courses:
            self.assertIsInstance(course_history, StudentCourseHistory)
            self.assertEqual(course_history.studentID, student.id)
