from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.inventory import (
    get_user_inventory_json,
    add_ingredient_to_user,
    remove_ingredient_from_user,
    get_user_inventory_quantities
)

inventory_views = Blueprint('inventory_views', __name__)

@inventory_views.route('/api/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    user_id = get_jwt_identity()
    inventory = get_user_inventory_quantities(user_id)
    return jsonify(inventory)

@inventory_views.route('/api/inventory/add', methods=['POST'])
@jwt_required()
def add_ingredient():
    user_id = get_jwt_identity()
    data = request.json
    ingredient = data.get('ingredient')
    if not ingredient:
        return jsonify({'error': 'Ingredient name is required'}), 400
    
    new_ingredient = add_ingredient_to_user(user_id, ingredient)
    return jsonify({
        'message': f'Added {ingredient} to inventory',
        'ingredient': new_ingredient.to_json()
    })

@inventory_views.route('/api/inventory/remove', methods=['POST'])
@jwt_required()
def remove_ingredient():
    user_id = get_jwt_identity()
    data = request.json
    ingredient = data.get('ingredient')
    quantity = data.get('quantity', 1)
    
    if not ingredient:
        return jsonify({'error': 'Ingredient name is required'}), 400
    
    removed_count = remove_ingredient_from_user(user_id, ingredient, quantity)
    return jsonify({
        'message': f'Removed {removed_count} {ingredient}(s) from inventory',
        'removed_count': removed_count
    })
