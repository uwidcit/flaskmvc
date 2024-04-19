from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from functools import wraps
from.index import index_views
# from App.controllers import Routine, User
from App.controllers.routine import *
from App.controllers.user import * # * <- can be replaced with function u need
from App.models import Routine, User

routine_views = Blueprint('routine_views', __name__, template_folder='../templates')

@routine_views.route('/routines', methods=['GET'])
@routine_views.route('/routines/<int:routineID>', methods=['GET'])
def routine_page(routineID=1):
    routines = get_all_routines() #routines = Routine.query.all()
    selected_routine = Routine.query.filter_by(id=routineID).first()
    # return render_template('routines.html', routines=routines, selected_routine)
    return render_template('routines.html') #just testing

@routine_views.route('/edit-name/<int:routineID>', methods=['POST'])
@jwt_required()
def editName_action(routineID):
    #rename routine name, show a message and reload
    new_name = request.form.get('new_name') #Get new name from the form
    if not new_name:
        flash('Invalid new name.')
        return redirect(url_for('routine_page'))
    
    if current_user.editRoutine(routineID, new_name):
        flash('Routine renamed successfully.')
    else:
        flash('Failed to rename Routine.')
    return redirect(request.referrer) #redirects to the page the user was on before making the request
    #return redirect(url_for('routine_page'))

@routine_views.route('/delete-routine/<int:routineID>', methods=['DELETE'])
@jwt_required()
def delete_routine(routineID):
    user = User.query.filter_by(username=get_jwt_identity()).first()
    routine = Routine.query.get(routineID)

    #not too sure about this part
    if not routine or routine.user.username != get_jwt_identity():
        return jsonify(error=f'routine {routineID} invalid or does not belong to {get_jwt_identity()}'), 401

    user.removeRoutine(routineID)
    return jsonify(message=f'{routine.name} was deleted.'), 200


# if __name__ == "__main__": 
#   app.run(host='0.0.0.0', port=8080)

    
