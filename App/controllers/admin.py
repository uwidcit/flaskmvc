from App.database import db
from App.models import admin, Competition, Team
from App.controllers.team import get_team_by_id

#Function to get admin
def get_admin(id):
    user = admin.query.get(id)
    return user

#Function to create a new competition
def create_competition(self, compName, startDate, endDate, teamID):
        new_comp = Competition(compName=compName, startDate=startDate, endDate=endDate, teamID = teamID)
        self.comps.append(new_comp)
        db.session.add(self)
        db.session.commit()
        return new_comp

#Function to update a competition
def update_competition(self, compCode, compName, startDate, endDate, teamID):
        for comp in self.comps:
            if comp.compCode == compCode:
                comp.compName = compName
                comp.startDate = startDate
                comp.endDate = endDate
                comp.teamID = teamID
        db.session.add(self)
        db.session.commit()
        return self.comps

#Function to delete a competition
def delete_competition(self, compCode):
        for comp in self.comps:
            if comp.compCode == compCode:
                self.comps.remove(comp)
        db.session.add(self)
        db.session.commit()
        return self.comps
      
#Function to create a new team 
def create_team(teamName, score):
    team = Team(teamName = teamName, score = score)
    db.session.add(team)
    db.session.commit()
    return team

#Function to update a team
def update_team(id, teamName, score): 
    team = get_team_by_id(id)
    if team:
        if teamName:
            team.name = teamName
        if score:
            team.score = score
        db.session.add(team)
        db.session.commit()
        return team
    return None

#Function to delete a team
def delete_team(id): 
    team = get_team_by_id(id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return True
    return False