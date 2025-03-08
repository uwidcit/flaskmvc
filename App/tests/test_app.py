import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from App.models import Building, Floor, Room
from App.controllers import building, floor, room
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

class BuildingUnitTests(unittest.TestCase):

    def test_new_building(self):
        building = Building("B1", "Main Building")
        self.assertEqual(building.building_id, "B1")
        self.assertEqual(building.building_name, "Main Building")


    def test_building_get_json(self):
        building = Building("B2", "Science Block")
        expected_json = {
            'building_id': "B2",
            'building_name': "Science Block"
        }
        self.assertDictEqual(building.get_json(), expected_json)

class FloorUnitTests(unittest.TestCase):

    def test_new_floor(self):
        floor = Floor("F1", "B1", "First Floor")
        self.assertEqual(floor.floor_id, "F1")
        self.assertEqual(floor.building_id, "B1")
        self.assertEqual(floor.floor_name, "First Floor")

    def test_floor_get_json(self):
        floor = Floor("F2", "B1", "Second Floor")
        expected_json = {
            'floor_id': "F2",
            'building_id': "B1",
            'floor_name': "Second Floor"
        }
        self.assertDictEqual(floor.get_json(), expected_json)

class RoomUnitTests(unittest.TestCase):

    def test_new_room(self):
        room = Room("R1", "F1", "Conference Room")
        self.assertEqual(room.room_id, "R1")
        self.assertEqual(room.floor_id, "F1")
        self.assertEqual(room.room_name, "Conference Room")

    def test_room_get_json(self):
        room = Room("R2", "F1", "Meeting Room")
        expected_json = {
            'room_id': "R2",
            'floor_id': "F1",
            'room_name': "Meeting Room"
        }
        self.assertDictEqual(room.get_json(), expected_json)

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
        
