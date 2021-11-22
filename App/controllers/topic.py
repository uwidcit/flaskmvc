from App.models import ( Topic )
from App.models.database import db

#create new topic
def create_topic(topic_id, topic_name, topic_description, date_timestamp):
    newTopic = Topic(topic_id = topic.id, topic_name = topic_name, topic_description = topic_description, date_timestamp = date_timestamp)
    print("Successfully Created")
    db.session.add(newTopic)
    db.session.commit()
    return newTopic

#create new subtopic
def create_subTopic(Maintopic_id, Subtopic_id , Subtopic_name, Subtopic_description, date_timestamp):
    newSubTopic = Topic(Maintopic_id = Maintopic_id,Subtopic_id=Subtopic_id, Subtopic_name = Subtopic_name, Subtopic_description = Subtopic_description, date_timestamp = date_timestamp)
    print("Successfully Created")
    db.session.add(newSubTopic)
    db.session.commit()
    return newSubTopic

# get topic by id
def get_topic_by_id(topic_id):
    print("getting Topic")
    order = Topic.query.filter(topic.id == topic_id).first() 
    return topic

#  get_topic_by_term
def get_topic_by_term(term):
    list_of_topic = []
    topic = Topic.query.filter(
        Topic.topic_name.contains(term)
    | Topic.topic_description.contains(term)
    | Topic.Subtopic_name.contains(term))
    if topic:
        list_of_topic = [o.toDict() for o in topic]
    return list_of_topic


# deleting subTopic by id
def delete_subTopic_by_id(Subtopic_id):
    print("deleting SubTopic")
    Subtopic = User.query.filter(Subtopic_id == Subtopic_id).first()
    if customer:
        db.session.delete(Subtopic)
        db.session.commit()
        return True
    return False