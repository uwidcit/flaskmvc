from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers.auth import jwt_required
from App.controllers.routine import *
from App.controllers.user import * # * <- can be replaced with function u need
from App.controllers.workout import *
from App.controllers.userWorkouts import *
from App.models import Routine, User, Workout, db

routine_views = Blueprint('routine_views', __name__, template_folder='../templates')


@routine_views.route('/routines',methods=['GET'])
def routine_page():
    
    routines=get_all_routines()
    
    return render_template('routines.html',routines=routines)


@routine_views.route('/create_routine',methods=['POST'])
def make_routine():
    data=request.form
    name=data['name']
    routine=create_routine(1,name)
    flash(f'Routine created: {data["name"]}')
    return redirect(request.referrer)


@routine_views.route('/edit-name', methods=['POST'])
def editName():
    data=request.form
    oldname=data['oldname']
    newname=data['newname']
    routine=renameRoutine(oldname,newname)
    return redirect(request.referrer)



@routine_views.route('/delete-routine/', methods=['DELETE'])
def delete_from_routine():
    data=request.form
    id=data['id']
    routine=delete_routine(id)
    flash('Routine deleted')
    return redirect(request.referrer)
    


    



    
