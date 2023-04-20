from App.database import db
from App.models import Competition

#Function to get competition by id
def get_competition_by_id(id):
    competition = Competition.query.get(id)
    return competition

#Function to get competition in json format
def get_competition_by_id_json(id):
    competition = Competition.query.get(id)
    return competition.to_json()

#Function to get all competitions
def get_all_competitions():
    competition = Competition.query.all()
    return competition

#Function to get all competitions in json format
def get_all_competitions_json():
    competition = Competition.query.all()
    return competition.to_json()

#Function to get competition by name
def get_competition_by_name(name):
    competition = Competition.query.filter_by(name = name).first()
    return competition

#Function to get competition by name in json format
def get_competition_by_name_json(name):
    competitions = Competition.query.filter_by(name = name).first()
    return [competition.to_json() for competition in competitions]

#Function to get Start Date
def get_start_date(id):
    competition = Competition.query.get(id)
    return competition.startDate

#Function to get End Date
def get_end_date(id):
    competition = Competition.query.get(id)
    return competition.endDate

#Function to delete competition
def delete_competition(id):
    competition = Competition.query.get(id)
    if competition:
        db.session.delete(competition)
        db.session.commit()
        return True
    return False