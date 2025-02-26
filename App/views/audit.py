from flask import Blueprint, render_template

audit_views = Blueprint('audit_views', __name__, template_folder='../templates')

@audit_views.route('/audit', methods=['GET'])
def inventory_page():
    return render_template('audit.html')