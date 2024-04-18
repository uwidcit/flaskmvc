from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import User, Workout, Routine

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    create_routine,
    get_all_routines,
    get_routine,
    get_user_routines,
    update_routine,
    add_workout_to_routine,
    delete_routine
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

# Create routines
@user_views.route('/routine/create', methods=['POST'])
@jwt_required
def create_routine2():
    data = request.json
    routine = create_routine(data['name'], data['description'], jwt_current_user.id)
    return jsonify(routine.get_json())

# Add workout to routine
@user_views.route('/routine/<int:routine_id>/add_workout', methods=['POST'])
@jwt_required
def add_workout(routine_id):
    workout_id = request.form.get('workout_id')
    add_workout_to_routine(routine_id, workout_id)
    return redirect(url_for('user_views.edit_routine2', id=routine_id))

# View/Edit routine
@user_views.route('/routine/edit/<int:id>', methods=['GET', 'POST'])
@jwt_required
def edit_routine2(id):
    routine = get_routine(id)
    if not routine or routine.user_id != jwt_current_user.id:
        return redirect(url_for('user_views.display_routines'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        updated_routine = update_routine(id, name=name, description=description)
        if updated_routine:
            return redirect(url_for('user_views.display_routines'))

    workouts = get_all_workouts()
    return render_template('routine_form.html', form_action=url_for('user_views.edit_routine2', id=id), routine=routine, workouts=workouts)

# Delete routine
@user_views.route('/routine/delete/<int:id>', methods=['POST'])
@jwt_required
def delete_routine2(id):
    routine = get_routine(id)
    if not routine or routine.user_id != jwt_current_user.id:
        return redirect(url_for('user_views.display_routines'))

    deleted_routine = delete_routine(id)
    if deleted_routine:
        return redirect(url_for('user_views.display_routines'))

    return 'Failed to delete routine', 400