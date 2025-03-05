from .user import create_user
from App.controllers.asset import *
from App.controllers.assetassignment import *
from App.controllers.assignee import *
from App.controllers.building import *
from App.controllers.floor import *
from App.controllers.history import *
from App.controllers.provider import *
from App.controllers.room import *
from App.controllers.scanevent import *

from datetime import datetime
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob@gmail.com','bob marley', 'bobpass')
    
    add_asset( 1, "Laptop", "ThinkPad X1", "Lenovo", "SN12345", 1, 1, datetime.now(), "Good condition", "Active")
    add_asset(2, "Projector", "Epson X300", "Epson", "SN67890", 2, 2, datetime.now(), "Mounted on ceiling", "Active")
    print("Assets created.")

    # Sample data for assetassignments
    create_asset_assignment(1, 1, 1, 1, datetime.now(), None)
    create_asset_assignment(2, 2, 2, 2, datetime.now(), None)
    print("Asset assignments created.")

    # Sample data for assignees
    create_assignee(1, "John", "Doe", "john.doe@mail.com")
    create_assignee(2, "Jane", "Smith", "jane.smith@mail.com")
    print("Assignees created.")

    # Sample data for buildings
    create_building(1, "Main Building")
    create_building(2, "Annex Building")
    print("Buildings created.")

    # Sample data for floors
    create_floor(1, 1, "1st Floor")
    create_floor(2, 2, "2nd Floor")
    print("Floors created.")
    

    # Sample data for history
    get_all_history_by_asset(1)
    get_all_history_by_asset(2)
    print("History records created.")

    # Sample data for providers
    create_provider(1, "Tech Supplies Ltd", "jerrysmith@techsupplies.com")
    create_provider(2, "Office Esstenials Inc", "support@officeessentials.com")
    print("Providers created.")

    # Sample data for rooms
    create_room(1, 1, "Asset Room: 101")
    create_room(2, 2, "Asset Room: 201")
    print("Rooms created.")

    #Sample data for scan events
    # add_scan_event(1, 1, datetime.now(), "Checked In", "Routine check")
    # add_scan_event(2, 2, datetime.now(), "Checked Out", "For external use")
    # print("Scan events created.")

    print("Sample data succesful.")

