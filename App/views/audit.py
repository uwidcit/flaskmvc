from flask import Blueprint, render_template, jsonify, request
from App.controllers.building import get_all_building_json
from App.controllers.floor import get_floors_by_building
from App.controllers.room import get_rooms_by_floor
from App.controllers.asset import get_all_assets_json

audit_views = Blueprint('audit_views', __name__, template_folder='../templates')

@audit_views.route('/audit')
def audit_page():
    buildings = get_all_building_json()
    return render_template('audit.html',
                          buildings=buildings)

@audit_views.route('/api/floors/<building_id>')
def get_floors(building_id):
    floors = get_floors_by_building(building_id)
    floors_json = [floor.get_json() for floor in floors]
    return jsonify(floors_json)

@audit_views.route('/api/rooms/<floor_id>')
def get_rooms(floor_id):
    rooms = get_rooms_by_floor(floor_id)
    rooms_json = [room.get_json() for room in rooms]
    return jsonify(rooms_json)

@audit_views.route('/api/assets/<room_id>')
def get_room_assets(room_id):
    all_assets = get_all_assets_json()
    room_assets = [asset for asset in all_assets if asset['room_id'] == int(room_id)]
    return jsonify(room_assets)