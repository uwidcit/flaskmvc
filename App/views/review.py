from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity

from App.controllers import *

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/api/reviews', methods=['POST'])
def create_review_action():
    data = request.json
    is_valid,message = validate_student_id(data['studentId'])
    if(is_valid):
        return message
    is_clean, message = validate_vote(data)
    if(is_clean==False):
        return message 
    if(create_review( data['message'], data['studentId'], data['upvote'], data['downvote'])):
        return jsonify({'message': f"review for: {data['studentId']} created"})
    else:
        return jsonify({'message': f"FAILED to create review for: {data['id']} "})
 
@review_views.route('/api/review/update', methods=['POST'])
def update_review_action():
    data = request.json
    is_clean, message = validate_vote(data)
    if(is_clean==False):
        return message 
    if(update_review(data['id'], data['upvote'], data['downvote'])):
        return jsonify({'message': f"review updated for id: {data['id']} "})
    else:
        return jsonify({'message': f"FAILED review updated for id: {data['id']} "})


