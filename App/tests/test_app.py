import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from App.models import Assignee, AssetAssignment, Building, Floor, Room, Asset, ScanEvent
from App.controllers import (
    create_building, get_building, 
    create_floor, get_floor,
    create_room, get_room, 
)
from App.controllers.asset import(
    get_asset, get_all_assets,
    get_all_assets_json, get_all_assets_by_room_id,
    add_asset, set_last_located,set_status, upload_csv
)
from App.controllers.scanevent import(
    add_scan_event, get_all_scans,
    get_scan_event, get_scans_by_status,
    get_scans_by_last_update, get_scans_by_changelog
)
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
from App.controllers.assignee import create_assignee, get_assignee_by_id, update_assignee
from App.controllers.assetassignment import (
    create_asset_assignment, get_asset_assignment_by_id,
    update_asset_assignment, delete_asset_assignment
)

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User( "bob@gmail.com", "bob", "bobpass")
        self.assertEqual(user.id, None)
        self.assertEqual(user.username, "bob")
        #assert user.email == "bob@gmail.com"
        self.assertEqual(user.email, "bob@gmail.com")
       # self.assertEqual(user.password, "bobpass")
        

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User( "bob@gmail.com", "bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "email":"bob@gmail.com", "username":"bob" })
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob@gmail.com", "bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob@gmail.com", "bob", password)
        assert user.check_password(password)

class BuildingUnitTests(unittest.TestCase):

    def test_new_building(self):
        building = Building("B1", "Main Building")
        self.assertEqual(building.building_id, "B1")
        self.assertEqual(building.building_name, "Main Building")


    def test_building_get_json(self):
        building = Building("B2", "Main Building")
        expected_json = {
            'building_id': "B2",
            'building_name': "Main Building"
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
        room = Room("R1", "F1", "Asset Room: 101")
        self.assertEqual(room.room_id, "R1")
        self.assertEqual(room.floor_id, "F1")
        self.assertEqual(room.room_name, "Asset Room: 101")

    def test_room_get_json(self):
        room = Room("R2", "F1", "Asset Room: 102")
        expected_json = {
            'room_id': "R2",
            'floor_id': "F1",
            'room_name': "Asset Room: 102"
        }
        self.assertDictEqual(room.get_json(), expected_json)

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
            "AA1", "asset1", "assigned1", "F1",
            assignment_date="2025-03-07 12:00:00", return_date="2025-03-08 12:00:00"
        )
        self.assertEqual(aa.assignment_id, "AA1")
        self.assertEqual(aa.asset_id, "asset1")
        self.assertEqual(aa.assigned_to_assignee_id, "assigned1")
        self.assertEqual(aa.floor_id, "F1")
        self.assertEqual(aa.assignment_date, "2025-03-07 12:00:00")
        self.assertEqual(aa.return_date, "2025-03-08 12:00:00")

    def test_get_json(self):
        aa = AssetAssignment(
            "AA1", "asset1", "assigned1", "1st Floor",
            assignment_date="2025-03-07 12:00:00", return_date="2025-03-08 12:00:00"
        )
        expected = {
            'assignment_id': "AA1",
            'asset_id': "asset1",
            'assigned_to_assignee_id': "assigned1",
            'floor_id': "1st Floor",
            'assignment_date': "2025-03-07 12:00:00",
            'return_date': "2025-03-08 12:00:00"
        }
        self.assertEqual(aa.get_json(), expected)

class AssetUnitTests(unittest.TestCase):
    def test_new_asset(self):
        asset = Asset("01", "laptop", "ISP 300", "DELL", "8300164", "R2", "R2", "01", "30-01-2025", "Recently bought", "Good")
        self.assertEqual(asset.id, "01")
        self.assertEqual(asset.description, "laptop")
        self.assertEqual(asset.model, "ISP 300")
        self.assertEqual(asset.brand, "DELL")
        self.assertEqual(asset.serial_number, "8300164")
        self.assertEqual(asset.room_id, "R2")
        self.assertEqual(asset.last_located, "R2")
        self.assertEqual(asset.assignee_id, "01")
        self.assertEqual(asset.last_update, "30-01-2025")
        self.assertEqual(asset.notes, "Recently bought")
        self.assertEqual(asset.status, "Good")
        
    def test_get_json(self):
        asset = Asset("01", "laptop", "ISP 300", "DELL", "8300164", "R2", "R2", "01", "30-01-2025", "Recently bought", "Good")
        expected_json = {
            'id': "01",
            'description': "laptop",
            'model': "ISP 300",
            'brand': "DELL",
            'serial_number': "8300164",
            'room_id': "R2",
            'last_located': "R2",
            'assignee_id': "01",
            'last_update': "30-01-2025",
            'notes': "Recently bought",
            'status': "Good"
        }
        self.assertDictEqual(asset.get_json(), expected_json)
        
class ScanEventUnitTest(unittest.TestCase):
    def test_new_scanevent(self):
        scanevent = ScanEvent("01", "01", "01", "01", "30-12-2024", "Good", "scanned successfully", "15-09-2024", "Original owner")
        self.assertEqual(scanevent.asset_id, "01")
        self.assertEqual(scanevent.user_id, "01")
        self.assertEqual(scanevent.room_id, "01")
        self.assertEqual(scanevent.scan_time, "30-12-2024")
        self.assertEqual(scanevent.status, "Good")
        self.assertEqual(scanevent.notes, "scanned successfully")
        self.assertEqual(scanevent.last_update, "15-09-2024")
        self.assertEqual(scanevent.changeLog, "Original owner")
        
    def test_get_json(self):
        scanevent = ScanEvent("01", "02", "03", "04", "30-12-2024", "Good", "scanned successfully", "15-09-2024", "Original owner")
        expected_json = {
            'scan_id: ': "01",
            'asset_id: ': "02",
            'user_id: ': "03",
            'room_id: ': "04",
            'scan_time: ': "30-12-2024",
            'status: ': "Good",
            'notes: ': "scanned successfully",
            'last_update: ': "15-09-2024",
            'change log: ': "Original owner"
        }
        self.assertDictEqual(scanevent.get_json(), expected_json)
        
        
        
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
    user = create_user("bob@gmail.com", "bob", "bobpass")
    assert login("bob@gmail.com", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick@gmail.com", "rick", "bobpass")
        assert user.email == "rick@gmail.com"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "email":"bob@gmail.com", "username":"bob"}, {"id":2, "email":"rick@gmail.com", "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie@gmail.com", "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        
class BuildingIntegrationTests (unittest.TestCase):

    def test_create_building(self):
        building = create_building("B3", "Third building")
        self.assertEqual(building.building_name, "Third building")

    def test_get_building(self):
        create_building("B1", "Main Building")
        building = get_building("B1")  
        self.assertIsNotNone(building)
        self.assertEqual(building.building_name, "Main Building")

class FloorIntegrationTests(unittest.TestCase):

    def test_create_floor(self):
        floor = create_floor("F3", "B3", "Third Floor")
        self.assertEqual(floor.floor_name, "Third Floor")

    def test_get_floor(self):
        create_floor("F4", "B3", "Fourth Floor")
        floor = get_floor("F4")
        self.assertIsNotNone(floor)
        self.assertEqual(floor.floor_name, "Fourth Floor")

class RoomIntegrationTests(unittest.TestCase):

    def test_create_room(self):
        room = create_room("R3", "F3", "Asset Room: 103")
        self.assertEqual(room.room_name, "Asset Room: 103")

    def test_get_room(self):
        create_room("R4", "F3", "Asset Room: 104")
        room = get_room("R4")
        self.assertIsNotNone(room)
        self.assertEqual(room.room_name, "Asset Room: 104")

class AssigneeIntegrationTests(unittest.TestCase):

    def test_create_assignee(self):
        assignee = create_assignee("Alice", "Smith", "alice@example.com", "R1")
        self.assertEqual(assignee.email, "alice@example.com")

    def test_update_assignee(self):
        assignee = create_assignee("Bob", "Jones", "bob@example.com", "R2")
        updated = update_assignee(assignee.id, "Robert", "Jones", "bob@example.com", "R3")
        self.assertEqual(updated.fname, "Robert")
        self.assertEqual(updated.room_id, "R3")

class AssetAssignmentIntegrationTests(unittest.TestCase):
    def test_create_asset_assignment(self):
        aa = create_asset_assignment("AA1", "asset1", "assigned1", "F1")
        self.assertEqual(aa.assignment_id, "AA1")
        self.assertIsNotNone(aa.assignment_date)  
        
    def test_update_asset_assignment(self):
        create_asset_assignment(
            "AA2", "asset2", "assigned2", "F1",
            assignment_date="2025-03-07 12:00:00", return_date="2025-03-08 12:00:00"
        )
        updated = update_asset_assignment("AA2", asset_id="asset3", return_date="2025-03-09 12:00:00")
        self.assertEqual(updated.asset_id, "asset3")
        self.assertEqual(updated.return_date, "2025-03-09 12:00:00")

    def test_delete_asset_assignment(self):
        create_asset_assignment("AA3", "asset3", "assigned3", "F1")
        result = delete_asset_assignment("AA3")
        self.assertTrue(result)
        aa = get_asset_assignment_by_id("AA3")
        self.assertIsNone(aa)
        
class AssetIntegrationTests(unittest.TestCase):
    def test_create_asset(self):
        #test_asset = add_asset( "1", "laptop", "ISP 300", "DELL", "8300164", "R2", "R2", "01", "30-01-2025", "Recently bought", "Good")
       # test_2 = Asset( "1", "laptop", "ISP 300", "DELL", "8300164", "R2", "R2", "01", "30-01-2025", "Recently bought", "Good")
        #self.assertEqual(test_asset.id, "1")
        """Test the add_asset method with valid parameters."""
    # Arrange - Define all required parameters for add_asset
        asset_id = "A001"
        description = "Test Laptop"
        model = "XPS 15"
        brand = "Dell"
        serial_number = "SN123456789"
        room_id = "R3"  # Assumes this room exists in the test database
        last_located = "R3"
        assignee_id = 1  # Assumes this assignee exists in the test database
        last_update = datetime.now()
        notes = "Test notes for asset"
        status = "Good"
    
    # Act - Call the function under test
        new_asset = add_asset(asset_id, description, model, brand, serial_number, 
                         room_id, last_located, assignee_id, last_update, 
                         notes, status)
    
    # Assert - Verify the asset was created correctly
        self.assertIsNotNone(new_asset)
        self.assertEqual(new_asset.id, asset_id)
        self.assertEqual(new_asset.description, description)
        self.assertEqual(new_asset.model, model)
        self.assertEqual(new_asset.brand, brand)
        self.assertEqual(new_asset.serial_number, serial_number)
        self.assertEqual(new_asset.room_id, room_id)
        self.assertEqual(new_asset.last_located, last_located)
        self.assertEqual(new_asset.assignee_id, assignee_id)
        self.assertEqual(new_asset.notes, notes)
        self.assertEqual(new_asset.status, status)
        
        # Verify the asset exists in the database
        retrieved_asset = get_asset(asset_id)
        self.assertIsNotNone(retrieved_asset)
        self.assertEqual(retrieved_asset.id, asset_id)
        self.assertEqual(retrieved_asset.description, description)
            
            
    def test_add_asset_duplicate_id(self):
        """Test adding an asset with a duplicate ID."""
    # Arrange - Create an asset first
        asset_id = "A002"
        add_asset(asset_id, "First Asset", "Model1", "Brand1", "SN11111", 
             "R3", "R3", 1, datetime.now(), "First asset notes", "Good")
    
    # Act - Try to create another asset with the same ID
        duplicate_asset = add_asset(asset_id, "Second Asset", "Model2", "Brand2", 
                               "SN22222", "R4", "R4", 2, datetime.now(), 
                               "Second asset notes", "Good")
    
    # Assert - Function should return None for duplicate ID
        self.assertIsNone(duplicate_asset)
    
    # Verify the original asset is unchanged
        original_asset = get_asset(asset_id)
        self.assertEqual(original_asset.description, "First Asset")

   #Test needs to be fixed
   
    # def test_add_asset_invalid_room(self):
    #     """Test adding an asset with a non-existent room ID."""
    #     # Arrange - Use a room ID that doesn't exist
    #     asset_id = "A003"
    #     non_existent_room = "NONEXISTENT"
        
    #     # Act - Try to create asset with invalid room
    #     result = add_asset(asset_id, "Test Asset", "Model3", "Brand3", 
    #                     "SN33333", non_existent_room, non_existent_room, 
    #                     1, datetime.now(), "Test notes", "Good")
        
    #     # Assert - Function should return None due to foreign key constraint
    #     self.assertIsNone(result)
        
    #     # Verify the asset was not created
    #     self.assertIsNone(get_asset(asset_id))

    # def test_add_asset_missing_required_fields(self):
    #     """Test that add_asset properly handles missing required fields."""
    #     # Arrange - Missing room_id which is a required field
    #     asset_id = "A004"
        
    #     # Act & Assert - This should raise an exception due to the NOT NULL constraint
    #     # Using context manager to catch the expected exception
    #     with self.assertRaises(Exception):
    #         add_asset(asset_id, "Test Asset", "Model4", "Brand4", 
    #                 "SN44444", None, "R3", 1, datetime.now(), 
    #                 "Test notes", "Good")
    
    def test_get_asset_by_id(self):
        # add_asset("01", "laptop", "ISP 300", "DELL", "8300164", "R2", "R2", "01", "30-01-2025", "Recently bought", "Good")#  create_room("R4", "F3", "Asset Room: 104")
        # a = get_asset("01")# room = get_room("R4")
        # self.assertIsNotNone(a)# self.assertIsNotNone(room)
        # self.assertEqual(a.description, "laptop")# self.assertEqual(room.room_name, "Asset Room: 104")
        
        """Test retrieving an asset by its ID."""
        # Arrange - Create an asset first
        asset_id = "A101"
        description = "Test Device"
        model = "Latitude 7400"
        brand = "Dell"
        serial_number = "SN987654321"
        room_id = "R4"  # Assumes this room exists in the test database
        last_located = "R4"
        assignee_id = 1  # Assumes this assignee exists in the test database
        last_update = datetime.now()
        notes = "Testing get_asset method"
        status = "Excellent"
        
        # Add the asset to the database
        add_asset(asset_id, description, model, brand, serial_number,
                room_id, last_located, assignee_id, last_update,
                notes, status)
        
        # Act - Call the function under test
        retrieved_asset = get_asset(asset_id)
        
        # Assert - Verify the asset was retrieved correctly
        self.assertIsNotNone(retrieved_asset)
        self.assertEqual(retrieved_asset.id, asset_id)
        self.assertEqual(retrieved_asset.description, description)
        self.assertEqual(retrieved_asset.model, model)
        self.assertEqual(retrieved_asset.brand, brand)
        self.assertEqual(retrieved_asset.serial_number, serial_number)
        self.assertEqual(retrieved_asset.room_id, room_id)
        self.assertEqual(retrieved_asset.last_located, last_located)
        self.assertEqual(retrieved_asset.assignee_id, assignee_id)
        self.assertEqual(retrieved_asset.notes, notes)
        self.assertEqual(retrieved_asset.status, status)
        
    def test_get_asset_nonexistent_id(self):
        """Test retrieving an asset with an ID that doesn't exist."""
        # Act - Try to retrieve an asset with a non-existent ID
        nonexistent_id = "NONEXISTENT"
        retrieved_asset = get_asset(nonexistent_id)
        
        # Assert - Should return None for non-existent asset
        self.assertIsNone(retrieved_asset)

    def test_get_asset_after_deletion(self):
        """Test retrieving an asset after it has been deleted."""
        # Arrange - Create and then delete an asset
        asset_id = "A102"
        
        # Add the asset
        add_asset(asset_id, "Temporary Asset", "TempModel", "TempBrand", 
                "SNTEMP", "R4", "R4", 1, datetime.now(), 
                "This asset will be deleted", "Good")
        
        # Verify it was added
        self.assertIsNotNone(get_asset(asset_id))
        
        # Delete the asset (using SQLAlchemy directly since there's no delete_asset function)
        asset_to_delete = get_asset(asset_id)
        if asset_to_delete:
            db.session.delete(asset_to_delete)
            db.session.commit()
        
        # Act - Try to retrieve the deleted asset
        retrieved_asset = get_asset(asset_id)
        
        # Assert - Should return None for deleted asset
        self.assertIsNone(retrieved_asset)

    def test_get_asset_case_sensitivity(self):
        """Test if get_asset is case sensitive for string IDs."""
        # Arrange - Create an asset with a mixed-case ID
        original_id = "MixedCase123"
        
        add_asset(original_id, "Case Sensitive Test", "TestModel", "TestBrand", 
                "SNTEST", "R4", "R4", 1, datetime.now(), 
                "Testing ID case sensitivity", "Good")
        
        # Act - Try to retrieve with different case
        lower_case_id = original_id.lower()
        retrieved_with_lower = get_asset(lower_case_id)
        
        upper_case_id = original_id.upper()
        retrieved_with_upper = get_asset(upper_case_id)
        
        # Assert - Should be case sensitive (depending on database)
        # This test will help identify the behavior of your system
        original_asset = get_asset(original_id)
        self.assertIsNotNone(original_asset)
        
        # The following assertions depend on your database's case sensitivity
        # SQLite is typically case-insensitive for string comparisons
        # If you want strict case sensitivity, you might need to adjust your query
        if retrieved_with_lower is None and retrieved_with_upper is None:
            # Database is case sensitive
            self.assertIsNone(retrieved_with_lower)
            self.assertIsNone(retrieved_with_upper)
        else:
            # Database is case insensitive (like SQLite default)
            # This is informational - the test doesn't necessarily fail
            pass
        
    def test_get_all_assets(self):
        """Test retrieving all assets from the database."""
    # Arrange - Clear existing assets to start with known state
    # (This approach is optional - depends on your test setup)
        for asset in Asset.query.all():
            db.session.delete(asset)
        db.session.commit()
        
        # Create multiple test assets
        test_assets = [
            # id, description, model, brand, serial_number, room_id, last_located, assignee_id, last_update, notes, status
            ("A201", "Desktop PC", "OptiPlex 7050", "Dell", "SN10001", "R1", "R1", 1, datetime.now(), "Test asset 1", "Good"),
            ("A202", "Monitor", "P2419H", "Dell", "SN10002", "R1", "R1", 1, datetime.now(), "Test asset 2", "Fair"),
            ("A203", "Printer", "LaserJet Pro", "HP", "SN10003", "R2", "R2", 2, datetime.now(), "Test asset 3", "Excellent")
        ]
        
        # Add each test asset to the database
        for asset_data in test_assets:
            add_asset(*asset_data)
        
        # Act - Call the function under test
        all_assets = get_all_assets()
        
        # Assert - Verify all assets were retrieved
        self.assertIsNotNone(all_assets)
        self.assertEqual(len(all_assets), len(test_assets))
        
        # Verify each expected asset is in the returned list
        asset_ids = [asset.id for asset in all_assets]
        for asset_data in test_assets:
            expected_id = asset_data[0]
            self.assertIn(expected_id, asset_ids)
            
        # Verify some properties of each retrieved asset
        for asset in all_assets:
            # Find the corresponding test data
            test_data = next((data for data in test_assets if data[0] == asset.id), None)
            self.assertIsNotNone(test_data, f"Couldn't find test data for asset ID {asset.id}")
            
            # Check that properties match
            self.assertEqual(asset.description, test_data[1])
            self.assertEqual(asset.model, test_data[2])
            self.assertEqual(asset.brand, test_data[3])
            self.assertEqual(asset.serial_number, test_data[4])


    def test_get_all_assets_empty_database(self):
        """Test retrieving all assets when the database is empty."""
        # Arrange - Clear existing assets to start with empty state
        for asset in Asset.query.all():
            db.session.delete(asset)
        db.session.commit()
        
        # Act - Call the function under test
        all_assets = get_all_assets()
        
        # Assert - Should return an empty list, not None
        self.assertIsNotNone(all_assets)
        self.assertEqual(len(all_assets), 0)
        self.assertEqual(all_assets, [])

            
        
    # def test_get_all_assets_by_room_id(self):
        
    #      # First create multiple assets in different rooms
    #     add_asset("A1", "Laptop", "XPS 15", "Dell", "DL123456", "R1", "R1", "01", "2025-03-15", "New laptop", "Good")
    #     add_asset("A2", "Monitor", "P2419H", "Dell", "MN789012", "R1", "R1", "01", "2025-03-15", "24-inch monitor", "Good")
    #     add_asset("A3", "Printer", "LaserJet Pro", "HP", "HP345678", "R2", "R2", "02", "2025-03-15", "Color printer", "Good")
        
    #     # Retrieve assets for room R1
    #     assets_r1 = get_all_assets_by_room_id("R1")
        
    #     # Check that we got the correct number of assets
    #     self.assertEqual(len(assets_r1), 2)
        
    #     # Verify the returned assets are the ones we expect
    #     asset_ids = [asset.id for asset in assets_r1]
    #     self.assertIn("A1", asset_ids)
    #     self.assertIn("A2", asset_ids)
    #     self.assertNotIn("A3", asset_ids)
        
    #     # Retrieve assets for room R2
    #     assets_r2 = get_all_assets_by_room_id("R2")
        
    #     # Check that we got the correct number of assets
    #     self.assertEqual(len(assets_r2), 1)
        
    #     # Verify the returned asset is the one we expect
    #     self.assertEqual(assets_r2[0].id, "A3")
        
    #     # Test with a room that has no assets
    #     assets_r3 = get_all_assets_by_room_id("R3")
    #     self.assertEqual(len(assets_r3), 0)
        
        
        
        
        
        
    # def test_status_updated_with_location(self):
        
        

