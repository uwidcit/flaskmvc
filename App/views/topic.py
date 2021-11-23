from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
import json

topic_views = Blueprint('topic_views', __name__, template_folder='../templates')

# from App.controllers import (
#     create_topic,
#     create_subTopic,
#     get_topic_by_id,
#     delete_subTopic_by_id,
# )

# # create Topic
# @topic_views.route('/create-topic', methods=["POST"])
# @jwt_required()
# def create_topic():
#     #topic_id
#     topic_name = request.json.get('topic_name')
#     topic_description = request.json.get('topic_description')
#     #date_timestamp
#     newTopic = create_topic(topic_id, topic_name, topic_description,date_timestamp)
#     return jsonify(Topic.toDict())

# # create SubTopic
# @topic_views.route('/create-topic', methods=["POST"])
# @jwt_required()
# def create_Subtopic():
#     #Maintopic_id
#     Subtopic_name = request.json.get('Subtopic_name')
#     Subtopic_description = request.json.get('Subtopic_description')
#     #date_timestamp
#     newTopic = create_subTopic(Maintopic_id, Subtopic_id, Subtopic_name,Subtopic_description,date_timestamp)
#     return jsonify(SubTopic.toDict())

# # get specific Topic by ID
# @topic_views.route('/topic_id', methods=["GET"])
# def get_topic_id():
#     Topic_id = request.args.get("id")
#     order = get_topic_by_id(Topic_id)
#     return jsonify(Topic.toDict())

# #Deletes topic from database and returns if it was successful
# @topic_views.route('/delete-subTopic', methods=["DELETE"])
# def delete_subTopic():
#     subTopic_id = request.args.get("sub_topic_id")
#     deleted = delete_subTopic_by_id(subTopic_id)
#     return jsonify({"deleted" : deleted})