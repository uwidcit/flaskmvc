from App.database import db
from App.models import Competition

#Function to get competition
def getCompetition():
    competition = competition.query.get(id)
    return competition

#Function to get competition in json format
def getCompetitionJson():
    competition = competition.query.get(id)
    return competition.to_json()

#Function to get all competitions
def getallCompetition():
    competition = competition.query.all()
    return competition

#Function to get all competitions in json format
def getallCompetitionJson():
    competition = competition.query.all()
    return competition.to_json()