from App.models import Topic
from . import db


# get all topics
def get_topics():
    return Topic.query.all()

# get topic by id
def get_topic_by_id(id):
    print(f"Getting Topic with ID: {id}")
    topic = Topic.query.filter_by(id=id).first()
    return topic

# Get top 5 topics by post count
def get_popular_topics():
    topics = get_topics()
    sorted(topics, key=lambda i: i.get_post_count())
    return topics[:5]
    

# create new topic
def create_topic(text, level):
    newTopic = Topic(text=text, level=level)
    print(f"Created topic: {text}")
    db.session.add(newTopic)
    db.session.commit()
    return newTopic


def edit_topic(topic_id, text, level):
    topic = get_topic_by_id(topic_id)

    if topic:
        topic.text = text
        topic.level = level

        print(f"Updated topic: {text}")
        db.session.add(topic)
        db.session.commit()
        return topic 
    else:
        return None


# Move to separate model class
# create new subtopic
def create_subTopic(maintopic_id, subtopic_name, subtopic_description, date_timestamp):
    newSubTopic = create_subTopic(maintopic_id=maintopic_id, subtopic_name=subtopic_name,
                                  subtopic_description=subtopic_description, date_timestamp=date_timestamp)
    print("Successfully Created")
    db.session.add(newSubTopic)
    db.session.commit()
    return newSubTopic



#  get_topic_by_term
def get_topic_by_term(term):
    list_of_topic = []
    topic = Topic.query.filter(
        Topic.text.contains(term)
        | Topic.level.contains(term)
        | Topic.Subtopic_name.contains(term))
    if topic:
        list_of_topic = [o.toDict() for o in topic]
    return list_of_topic


# Delete topic by id
def delete_topic_by_id(id):
    print(f"Deleting topic with id: {id}")
    topic = get_topic_by_id(id)
    if topic:
        db.session.delete(topic)
        db.session.commit()
        return topic
    return None


# get topic by levelid
def get_topic_by_level(topiclvl_id):
     print("getting Topic")
     topic_lvl = Topic.query.filter(Topic.level == topiclvl_id).first() 
     if topic_lvl:
        return topic_lvl
    else:
        raise Exception("Topic not found")
