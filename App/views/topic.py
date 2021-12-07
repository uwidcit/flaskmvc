from App.modules.serialization_module import serialize_list
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required



from App.controllers.topic import (
    edit_topic,
    get_popular_topics,
    get_topics,
    create_topic,
    get_topic_by_id,
    delete_topic_by_id,
    get_topic_by_level
)

topic_views = Blueprint('topic_views', __name__, template_folder='../templates')


# Get all topics
@topic_views.route('/topics', methods=["GET"])
@jwt_required()
def get_all_topics():
    filter_popular = request.args.get('popular')

    if filter_popular:
        topics = get_popular_topics()
    else:
        topics = get_topics()
    topics = serialize_list(topics)
    return jsonify(topics)

# create Topic
@topic_views.route('/topics', methods=["POST"])
@jwt_required()
def create_new_topic():
    text = request.json.get('text')
    level = request.json.get('level')
    topic = create_topic(text, level)
    if topic:
        return jsonify(topic)
    else:
        
        return 201



# edit Topic
@topic_views.route('/topics/<int:topic_id>', methods=["PUT"])
@jwt_required()
def update_topic(topic_id):
    text = request.json.get('text')
    level = request.json.get('level')
    
    topic = edit_topic(topic_id, text, level)
    if topic:
        return jsonify(topic)
    else: 
        return 200


# get specific Topic by ID
@topic_views.route('/topics/<int:topic_id>', methods=["GET"])
def get_topic(topic_id):
    topic = get_topic_by_id(topic_id)
    return jsonify(topic.toDict())


#Deletes topic from database and returns if it was successful
@topic_views.route('/topics/<int:topic_id>', methods=["DELETE"])
def delete_topic(topic_id):
    result = delete_topic_by_id(topic_id)
    return jsonify(result.toDict()) if result else 404

#get all popular topics
@topic_views.route('/topics', methods=["GET"])
def popular_topics():
    popular_topic = get_popular_topics()
    return jsonify(popular_topic.toDict())if popular_topic else 404


#get all topics by level 
@topic_views.route('/topics', methods=["GET"])
def topic_level():
    level_topics= get_topic_by_level()
    return jsonify(serialize_list(level_topics)) if level_topics else 404
