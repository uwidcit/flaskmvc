from flask import Blueprint, render_template

home_views = Blueprint('home_views', __name__, template_folder='../templates')

@home_views.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')