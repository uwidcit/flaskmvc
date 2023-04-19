from App.database import db
from App.models import competition

#Function to get competition
def get_competition_by_id(id):
    competition = competition.query.get(id)
    return competition

#Function to get competition in json format
def get_competition_by_id_json(id):
    competition = competition.query.get(id)
    return competition.to_json()

#Function to get all competitions
def get_all_competition():
    competition = competition.query.all()
    return competition

#Function to get all competitions in json format
def get_all_competition_json():
    competition = competition.query.all()
    return competition.to_json()

#Function to get competition by name
def get_competition_by_Name(name):
    competition = competition.query.fliter_by(name = name).all()
    return competition

#Function to get competition by name in json format
def get_competition_by_name(name):
    competition = competition.query.fliter_by(name = name).all()
    return [competition.to_json() for competition in competition]

#Function to get Start Date
def get_start_date(id):
    competition = competition.query.get(id)
    return competition.startDate

#Function to get End Date
def get_end_date(id):
    competition = competition.query.get(id)
    return competition.endDate

#Function to delete competition
def delete_competition(id):
    competition = competition.query.get(id)
    if competition:
        db.session.delete(competition)
        db.session.commit()
        return True
    return False