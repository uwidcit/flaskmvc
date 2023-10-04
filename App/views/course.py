from flask import Blueprint, jsonify, request

from App.controllers import create_course

course_views = Blueprint('course_views', __name__, template_folder='../templates')

@course_views.route('/courses/<filename>', methods=['POST'])
def upload_course():
    try:
        data = request.get_json()

        if not all(key in data for key in ('file_path',)):
            return jsonify({'error': 'Invalid request data'}), 400

        file_path = data['file_path']
        new_course = create_course(file_path)

        return jsonify({'message': f'Course {new_course.courseCode} created successfully'}), 201

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 50

    
    