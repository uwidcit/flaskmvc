from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_user,
    create_program,
    create_programCourse,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    addSemesterCourses
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/addProgram/<name>/<core>/<elective>/<foun>',
                   methods=['POST'])
@login_required
def addProgram(name, core, elective, foun):
  newprogram = create_program(name, core, elective, foun)
  return jsonify({'message': f"Program {newprogram['name']} added"
                  }) if newprogram else 200


@staff_views.route('/staff/addProgramReq/<name>/<code>/<num>',
                   methods=['POST'])
@login_required
def addProgramRequirements(name, code, num):
  create_programCourse(name, code, num)
  return jsonify({'message': f"Program added"})


@staff_views.route('/staff/addNextSemesterCourse/<courseCode>',
                   methods=['POST'])
@login_required
def addCourse(courseCode):
  course = addSemesterCourses(courseCode)
  return jsonify({'message': f"Course {course['courseName']} added"}) if course else 200