from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash
from App.models import db
from App.controllers.auth import jwt_required
from App.controllers.workout import *
from App.controllers.userWorkouts import *
from App.controllers.routine import *
import json



workout_views= Blueprint('workout_views', __name__, template_folder='../templates')


@workout_views.route('/workout/<data>', methods=['GET'])
def work_page(data):
    workouts=get_workout_by_type(data)
    routines=get_all_routines()


    return render_template('workouts.html',workouts=workouts,routines=routines)


@workout_views.route('/save_workout', methods=['POST'])
def save_workout():
    data=request.form
    
    workout=addToRoutine(data['routine_id'],data['workout_id'])
    flash(f'{data["muscle_type"]}: {data["workout"]} saved')
    return redirect(request.referrer)



@workout_views.route('/remove_workout', methods=['DELETE'])
@jwt_required()
def delete_workout():
    data=request.form
    current_user.delete_workout(data['WorkOut'])

    flash(f'{data["WorkOut"]} deleted')
    return render_template(request.referrer)


    
