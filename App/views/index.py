# from flask import Blueprint, render_template, request, flash, redirect, url_for, session
# from flask_login import login_required
# from App.models import db
# from App.controllers import create_user

# index_views = Blueprint('index_views', __name__, template_folder='../templates')

# @index_views.route('/', methods=['GET'])
# def index_page():
#     return render_template('index.html')

# @index_views.route('/init', methods=['GET'])
# def init():
#     db.drop_all()
#     db.create_all()
#     create_user('bob', 'bobpass')
#     return jsonify(message='db initialized!')

# @index_views.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({'status':'healthy'})

#initial commit message

from flask import (
    Blueprint,
    render_template,
    jsonify,
)

index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")


@index_views.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})