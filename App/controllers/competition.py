from App.models import Competition, CompetitionResult
from App.database import db
from datetime import datetime

def create_competition(competition_Name, date_occurred, competition_description=None):
    competition = Competition(competition_Name=competition_Name, date_occurred=date_occurred, competition_description=competition_description)
    db.session.add(competition)
    db.session.commit()
    return competition

def get_all_competitions():
    return Competition.query.all()

def get_competition_by_id(compID):
    return Competition.query.get(compID)

def import_competition_results(compID, file_path):
    competition = get_competition_by_id(compID)
    if not competition:
        print(f"Competition with ID {compID} not found.")
        return False, None
    
    imported_results = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 2:
                    print(f"Skipping malformed line: {line.strip()}")
                    continue
                student, result = parts
                try:
                    comp_result = CompetitionResult(competition_id=compID, student=student, result=float(result))
                    db.session.add(comp_result)
                    imported_results.append(comp_result)  # collect and display later
                except ValueError:
                    print(f"Error parsing result for student {student}")
                    continue
        db.session.commit()
        return True, imported_results  # success - display results
    except Exception as e:
        print(f"An error occurred during import: {e}")
        return False, None  # fail - no results


def get_competition_results(compID):
    competition = get_competition_by_id(compID)
    if competition:
        return competition.results
    return None
