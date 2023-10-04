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
    addSemesterCourses
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/addNextSemesterCourse/<courseCode>', methods=['POST'])
def addCourse(courseCode):
    course = addSemesterCourses(courseCode)
    return jsonify({'message': f"Course {course['courseName']} added"}) if course else 200



    

