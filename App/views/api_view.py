from flask import Blueprint, render_template

api_bp = Blueprint('api_views', __name__, template_folder='../templates')

@api_bp.route('/', methods=['GET'])
def get_api_docs():
    return render_template('index.html')