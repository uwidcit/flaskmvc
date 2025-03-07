from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers.asset import get_all_assets_json

inventory_views = Blueprint('inventory_views', __name__, template_folder='../templates')

@inventory_views.route('/inventory', methods=['GET'])
@jwt_required()
def inventory_page():
    return render_template('inventory.html')

@inventory_views.route('/api/assets', methods=['GET'])
@jwt_required()
def get_assets():
    assets = get_all_assets_json()
    return jsonify(assets)

@inventory_views.route('/add-asset', methods=['GET'])
@jwt_required()
def add_asset_page():
    # This will be implemented in the future
    return render_template('message.html', 
                          title="Add Asset", 
                          message="Add Asset functionality coming soon!")