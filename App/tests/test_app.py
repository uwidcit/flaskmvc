import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.models import Prerequisites, ProgramCourses, StudentCourseHistory, Course
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    create_course,
    create_prereq,
    getPrereqCodes,
    create_program,
    create_programCourse,
    get_all_programCourses,
    get_program_by_name,
    programCourses_SortedbyRating,
    programCourses_SortedbyHighestCredits
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

    def test_new_prerequisite(self):
        prereq=Prerequisites("INFO2605","Introduction to Information Technology Concepts")
        assert prereq.prereq_courseCode=="INFO2605"

    def test_prerequisite_toJSON(self):
        prereq=Prerequisites("INFO2605","Introduction to Information Technology Concepts")
        prereq_json=prereq.get_json()
        self.assertDictEqual(prereq_json,{'prereq_id': None, 'prerequisite_courseCode': 'INFO2605', 'prerequisite_course': 'Introduction to Information Technology Concepts'})

    def test_new_program_course(self):
        programcourse=ProgramCourses("1","INFO2605","2")
        assert programcourse.code=="INFO2605"

    def test_program_course_toJSON(self):
        programcourse=ProgramCourses("1","INFO2605","2")
        programcourse_json=programcourse.get_json()
        self.assertDictEqual(programcourse_json,{'Program Course ID:':None, 'Program ID:':'1','Course Code: ':'INFO2605','Course Type: ':'2'})

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

    def test_create_prerequisite(self):
        file_path="testData/courseData.csv"
        create_course(file_path)

        create_prereq("MATH1115","Industrial Statistics")
        prereqs=getPrereqCodes("Industrial Statistics")
        self.assertEqual(['MATH1115'],prereqs)

    def test_create_program_requirement(self):
        program=create_program("Computer Science and Statistics",51,30,9)
        create_programCourse("Computer Science and Statistics","MATH1115",1)
        program_courses=get_all_programCourses("Computer Science and Statistics")
        assert any(course.code == "MATH1115" for course in program_courses)

    def test_programCourses_sorted_by_credits(self):        
        create_programCourse("Computer Science and Statistics","INFO2606",2)
        program=get_program_by_name("Computer Science and Statistics")
        credits_sorted=programCourses_SortedbyHighestCredits(program.id)
        self.assertListEqual(credits_sorted,['INFO2606', 'MATH1115'])   

    def test_programCourses_sorted_by_rating(self):
        create_programCourse("Computer Science and Statistics","MATH2250",1)
        program=get_program_by_name("Computer Science and Statistics")
        rating_list=programCourses_SortedbyRating(program.id)
        self.assertListEqual(rating_list,['MATH1115', 'INFO2606', 'MATH2250'])