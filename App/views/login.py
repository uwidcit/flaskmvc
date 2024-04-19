from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

login_views = Blueprint('login_views', __name__, template_folder='../templates')


@login_views.route('/',methods=['GET'])
def login_page():
    return render_template('login.html')