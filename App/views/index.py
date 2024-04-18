import os, csv
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

def initialize_db():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')

    # Load workouts from CSV file
    with open('workouts.csv', encoding='unicode_escape') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            workout = Workout(exercise_name=row['Exercise_Name'], 
                              exercise_image1=row['Exercise_Image'], 
                              exercise_image2=row['Exercise_Image1'], 
                              muscle_group=row['muscle_gp'], 
                              equipment=row['Equipment'], 
                              rating=float(row['Rating']), 
                              description=row['Description'])
            db.session.add(workout)
    db.session.commit()

    # Print workouts to console
    workouts = Workout.query.all()
    for workout in workouts:
        print(workout.get_json())

@index_views.route('/', methods=['GET'])
@index_views.route("/index/<user_id>", methods=["GET"])
def index_page(user_id=None):
    workouts = Workout.query.all()
    workout = Workout.query.get(user_id)
    print (workout)
    return render_template("index.html",current_user=current_user,workouts=workouts,workout=workout,
    )

@index_views.route('/init', methods=['GET'])
def init():
    initialize_db()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})