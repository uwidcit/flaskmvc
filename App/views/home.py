from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.recipe import get_user_recipes
from App.controllers.inventory import get_user_inventory_quantities

home_views = Blueprint('home_views', __name__, template_folder='../templates')

@home_views.route('/home', methods=['GET'])
@jwt_required()
def home_page():
    user_id = get_jwt_identity()
    recipes = get_user_recipes(user_id)
    inventory = get_user_inventory_quantities(user_id)
    return render_template('home.html', recipes=recipes, inventory=inventory)
