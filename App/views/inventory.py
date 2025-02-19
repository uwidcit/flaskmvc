from flask import Blueprint, render_template

inventory_views = Blueprint('inventory_views', __name__, template_folder='../templates')

@inventory_views.route('/inventory', methods=['GET'])
def inventory_page():
    return render_template('inventory.html')
