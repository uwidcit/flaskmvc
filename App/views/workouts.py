from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

workout_views= Blueprint('workout_views', __name__, template_folder='../templates')



@workout_views.route('/workouts', methods=['GET'])
def workout_page():
    return render_template('workout.html')