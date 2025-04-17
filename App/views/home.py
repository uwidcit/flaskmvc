from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers.recipe import get_user_recipes

home_views = Blueprint('home_views', __name__, template_folder='../templates')

@home_views.route('/home', methods=['GET'])
def home_page():
    # Hardcode user_id=1 (for Bob) for demonstration/testing purposes
    bob_id = 1
    recipes = get_user_recipes(bob_id)
    return render_template('home.html', recipes=recipes)
