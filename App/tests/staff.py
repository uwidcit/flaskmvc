import unittest
from App.models import Staff
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