from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
import json

topic_views = Blueprint('topic_views', __name__, template_folder='../templates')

from App.controllers import (
     create_topic,
     update_topic,
     get_topic_by_id,
     delete_topic_by_id,
     get_topics,
     get_topic_by_level

)

 # create Topic
@topic_views.route('/create-topic', methods=["POST"])
@jwt_required()
def create_user_topic():
     topic_data = request.json.get('topic_data')
     topic_level = request.json.get('topic_level')
     newTopic = create_topic(topic_data, topic_level)
     return jsonify(Topic.toDict())

 # update Topic
@topic_views.route('/update-topic', methods=["POST"])
@jwt_required()
def update_user_topic():
     topic_data = request.json.get('topic_data')
     topic_level = request.json.get('topic_level')
     topic_id = request.args.get("topic_id")
     update_topic = create_topic(topic_id,topic_data,topic_level)
     return jsonify(Topic.toDict())

 # get specific Topic by ID
@topic_views.route('/topic_id', methods=["GET"])
def get_topic_id():
     topic_id = request.args.get("id")
     topic = get_topic_by_id(topic_id)
     return jsonify(Topic.toDict())


#Deletes topic from database and returns if it was successful
@topic_views.route('/delete-subTopic', methods=["DELETE"])
def delete_subTopic():
     topic_id = request.args.get("topic_id")
     deleted = delete_topic_by_id(topic_id)
     return jsonify({"deleted" : deleted})

# get all topics
@order_views.route('/topics', methods=["GET"])
@jwt_required()
def display_topics():
    topiclist = get_topics()
    return jsonify(topiclist)


 # get  Topic by level id
 #not entirely sure about this method
@topic_views.route('/topic_level', methods=["GET"])
def get_topic_levelid():
     topic_level = request.args.get("topic_level")
     level = get_topic_by_level(topic_level)
     return jsonify(Topic.toDict())