from App.models import ( Topic, db )


# #create new topic, ID and time stamp will be done in DB
def create_topic(topic_text,topic_lvl):
     newTopic = Topic(text = topic_text, level = topic_lvl,)
     print("Successfully Created")
     db.session.add(newTopic)
     db.session.commit()
     return newTopic

#update a topic that already exist
def update_topic(topic_id, topic_text , topic_lvl):
    print("getting Topic")
    topic_update = Topic.query.filter(topic.id == topic_id).first()
    topic_update.text = topic_text
    topic_update.level = topic_lvl
    db.session.add(topic_update)
    return topic_update

# delete Topic by id
def delete_topic_by_id(topic_id):
     print("deleting SubTopic")
     topic = Topic.query.filter(Topic.id ==topic_id).first()
     if topic:
         db.session.delete(topic)
         db.session.commit()
         return True
     return False

# get topic by id
def get_topic_by_id(topic_id):
     print("getting Topic")
     order = Topic.query.filter(Topic.id == topic_id).first() 
     return topic


# get list of ALL topics
def get_topics():
    print('get all orders')
    topics = Topic.query.all()
    list_of_topics = []
    if orders:
        list_of_topics = [o.toDict() for o in topics]
    return list_of_topics

 # get topic by id
def get_topic_by_level(topiclvl_id):
     print("getting Topic")
     topic_lvl = Topic.query.filter(Topic.level == topiclvl_id).first() 
     return topic_lvl