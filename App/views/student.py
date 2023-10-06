from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from.index import index_views

from App.controllers import (
    #create_user,
    #jwt_authenticate, 
    #get_all_users,
    #get_all_users_json,
    jwt_required,
    create_student,
    get_program_by_name,
    get_student_by_id,
    get_course_by_courseCode,
    addCoursetoHistory,
    create_easy_plan,
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

##Create student
@student_views.route('/student', methods=['POST'])
@jwt_required()
def create_student_route():
    student_id = request.json['student_id']
    password = request.json['password']
    name = request.json['name']
    programname = request.json['programname']

    student = get_student_by_id(student_id)
    if student:
        return jsonify({'error': 'Student id found'})
    
    program = get_program_by_name(programname)
    if not program:
        return jsonify({'Error': 'Incorrect program name'})

    create_student(student_id, password, name, programname)
    return jsonify({'Success!': f"user {student_id} created"})
    
##Add course to course history

@student_views.route('/student/add_course', methods=['POST'])
def add_course_to_student_route():
    student_id = request.json['student_id']
    course_code = request.json['course_code']

    if not student_id or not course_code:
        return jsonify({'error': 'Missing required fields'})

    # Check if the student and course exist
    student = get_student_by_id(student_id)
    course = get_course_by_courseCode(course_code)

    if not student:
        return jsonify({'error': 'Student not found'})
    if not course:
        return jsonify({'error': 'Course not found'})

     ##need error checking for whether course already in history

    addCoursetoHistory(student_id, course_code)
    return jsonify({'Success!': f"Course {course_code} added to student {student_id}'s course history"})


##Add course plan 

@student_views.route('/student/add_easy_plan', methods=['POST'])
def add_easy_plan():
    student_id = request.json['student_id']
    #Maybe pass in a string to determine which func to use."easy, fast, elec"
    # Check if the student exist
    student = get_student_by_id(student_id)

    if not student:
        return jsonify({'error': 'Student not found'})
    
    create_easy_plan(student)
    return jsonify({'Success!': f"Easy plan added to student {student_id} "})
