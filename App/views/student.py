from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    create_student,
    get_program_by_name,
    get_student_by_id,
    get_course_by_courseCode,
    addCoursetoHistory,
    getCompletedCourseCodes,
    generator,
    addCourseToPlan,
    verify_student
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

##Create student
@student_views.route('/student', methods=['POST'])
def create_student_route():
    student_id = request.json['student_id']
    password = request.json['password']
    name = request.json['name']
    programname = request.json['programname']

    if not all([student_id, password, name, programname]):
        return jsonify({'Error': 'Missing required fields. Please provide student id, password, name, and program name.'}), 400

    student = get_student_by_id(student_id)
    if student:
        return jsonify({'Error': 'Student id found'}), 400
    
    program = get_program_by_name(programname)
    if not program:
        return jsonify({'Error': 'Incorrect program name'}), 400

    create_student(student_id, password, name, programname)
    return jsonify({'Success!': f"user {student_id} created"}), 201
    
##Add course to course history

@student_views.route('/student/add_course', methods=['POST'])
@login_required
def add_course_to_student_route():
    student_id = request.json['student_id']
    course_code = request.json['course_code']

    username=current_user.username
    if not verify_student(username):    #verify that the user is logged in
        return jsonify({'message': 'You are unauthorized to perform this action. Please login with Student credentials.'}), 401
    
    if not student_id or not course_code:
        return jsonify({'Error': 'Missing required fields'}), 400

    # Check if the student and course exist
    student = get_student_by_id(student_id)
    course = get_course_by_courseCode(course_code)

    if not student:
        return jsonify({'Error': 'Student not found'}), 400
    if not course:
        return jsonify({'Error': 'Course not found'}), 400

    # Check if the course is already in the student's completed courses
    completed_courses = getCompletedCourseCodes(student_id)
    if course_code in completed_courses:
        return jsonify({'Error': 'Course already completed'}), 400

    addCoursetoHistory(student_id, course_code)
    return jsonify({'Success!': f"Course {course_code} added to student {student_id}'s course history"}), 200


##Add course plan 

@student_views.route('/student/create_student_plan', methods=['POST'])
@login_required
def create_student_plan_route():
    student_id = request.json['student_id']
    command = request.json['command']

    username=current_user.username
    if not verify_student(username):    #verify that the student is logged in
        return jsonify({'message': 'You are unauthorized to perform this action. Please login with Student credentials.'}), 401
    
    student = get_student_by_id(student_id)

    if not student:
        return jsonify({'Error': 'Student not found'}), 400
    
    valid_command = ["electives", "easy", "fastest"]

    if command in valid_command:
        courses = generator(student, command)
        return jsonify({'Success!': f"{command} plan added to student {student_id} ", "courses" : courses}), 200

    course = get_course_by_courseCode(command)
    if course:
        addCourseToPlan(student, command)
        return jsonify({'Success!': f"Course {command} added to student {student_id} plan"}), 200
    
    return jsonify("Invalid command. Please enter 'electives', 'easy', 'fastest', or a valid course code."), 400



    
