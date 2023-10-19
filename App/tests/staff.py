import unittest, pytest
from App.main import create_app
from App.database import db, create_db
from App.models import Staff
from App.controllers import create_staff, get_staff_by_id, login
from werkzeug.security import generate_password_hash

class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        staffid = 999
        staffName = "Jane Doe"
        staffpass = "janepass"
        staff = Staff(staffpass, staffid, staffName)
        self.assertEqual(staff.name, staffName)
        self.assertEqual(staff.id, staffid)
        
    def test_staff_toJSON(self):
        staffid = 999
        staffName = "Jane Doe"
        staffpass = "janepass"

        staff = Staff(staffpass, staffid, staffName)
        staff_json = staff.get_json()

        self.assertDictEqual(staff_json, {
            'staff_id': staffid,
            'name': staffName,
            })
    
    def test_set_password(self):
        password = "mypass"
        staff = Staff(password, 999, "Jane Doe")
        assert staff.password != password

    def test_check_password(self):
        password = "mypass"
        staff = Staff(password, 999, "Jane Doe")
        assert staff.check_password(password)

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class StaffIntegrationTests(unittest.TestCase):
    def test_create_staff(self):
        staffid = 9
        staffName = "Jane Doe"
        staffpass = "janepass"
        staff = create_staff(staffpass, staffid, staffName)

        assert staff is not None
        assert get_staff_by_id(9) != None
        

    