import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from App.models import Assignee, AssetAssignment
from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.email == "bob"

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

class AssigneeUnitTests(unittest.TestCase):
    def test_new_assignee(self):
        a = Assignee("Alice", "Smith", "alice@example.com", room_id="R1")
        self.assertEqual(a.fname, "Alice")
        self.assertEqual(a.lname, "Smith")
        self.assertEqual(a.email, "alice@example.com")
        self.assertEqual(a.room_id, "R1")

    def test_get_json(self):
        a = Assignee("Alice", "Smith", "alice@example.com", room_id="R1")
        expected = {
            'id': None,
            'fname': "Alice",
            'lname': "Smith",
            'email': "alice@example.com",
            'room_id': "R1"
        }
        self.assertEqual(a.get_json(), expected)

class AssetAssignmentUnitTests(unittest.TestCase):
    def test_new_asset_assignment(self):
        aa = AssetAssignment(
            "AA1", "asset123", "assignee123", "F1",
            assignment_date="2025-03-07 12:00:00", return_date="2025-03-08 12:00:00"
        )
        self.assertEqual(aa.assignment_id, "AA1")
        self.assertEqual(aa.asset_id, "asset123")
        self.assertEqual(aa.assigned_to_assignee_id, "assignee123")
        self.assertEqual(aa.floor_id, "F1")
        self.assertEqual(aa.assignment_date, "2025-03-07 12:00:00")
        self.assertEqual(aa.return_date, "2025-03-08 12:00:00")

    def test_get_json(self):
        aa = AssetAssignment(
            "AA1", "asset123", "assignee123", "F1",
            assignment_date="2025-03-07 12:00:00", return_date="2025-03-08 12:00:00"
        )
        expected = {
            'assignment_id': "AA1",
            'asset_id': "asset123",
            'assigned_to_assignee_id': "assignee123",
            'floor_id': "F1",
            'assignment_date': "2025-03-07 12:00:00",
            'return_date': "2025-03-08 12:00:00"
        }
        self.assertEqual(aa.get_json(), expected)

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
        assert user.email == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

