from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity

from App.controllers import *

student_views = Blueprint('student_views', __name__, template_folder='../templates')



# @student_views.route('/students', methods=['GET'])
# def get_user_page():
#     users = get_all_users()
#     return render_template('users.html', users=users)

@student_views.route('/api/students', methods=['GET'])
def get_students_action():
    students = get_all_students()
    return jsonify(students)

# @student_views.route('/api/students', methods=['GET'])
# def get_student_action():
#     students = get_all_students()
#     return jsonify(students)


@student_views.route('/api/students', methods=['POST'])
def create_student_action():
    data = request.json
    is_valid,message = validate_student_id(data['studentId'])
    if(is_valid):
        return message
    valid = create_student(data['studentId'], data['name'])
    if (valid == False):
        return jsonify({'message': f"failed to create Student with id: {data['studentId']}"})
    return jsonify({'message': f"student {data['studentId']} created"})

@student_views.route('/api/students', methods=['PUT'])
def update_student_action():
    data = request.json
    is_valid,message = validate_student_id(data['studentId'])
    if(is_valid):
        return message    
    value = update_student(data["studentId"], data['name'])
    if (value == False):
        return jsonify({'message': f"failed to update name:  {data['name']} "})
    else:
        return jsonify({'message': f"student name updated to:  {data['name']} "})

@student_views.route('/api/student', methods=['GET', 'POST'])
def get_student_action():
    data = request.json
    student = get_student_toJSON(data['studentId'])
    return jsonify({'message': f"Student found:{data['studentId']} with name: {student['name']}"} )


# @user_views.route('/identify', methods=['GET'])
# @jwt_required()
# def identify_user_action():
#     return jsonify({'message': f"username: {current_identity.username}, id : {current_identity.id}"})

# @user_views.route('/static/users', methods=['GET'])
# def static_user_page():
#   return send_from_directory('static', 'static-user.html')