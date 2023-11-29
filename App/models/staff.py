from App.database import db
from App.models import Programme

class Staff(User):
    dept = db.Column(db.String(50))
    faculty = db.Column(db.String(50))

    def create_programme(self, name):
        existing_programme = Programme.query.filter_by(degree_name=name).first()

        if existing_programme:
            return existing_programme
        else:
            new_programme = Programme(degree_name=name)
            db.session.add(new_programme)
            db.session.commit()
            return new_programme

        programme = Programme(degree_name=name)
        db.session.add(programme)
        db.session.commit()
        return programme

    def delete_programme(self, programme_id):
        programme = Programme.query.get(programme_id)
        if programme:
            db.session.delete(programme)
            db.session.commit()
            return True
        else:
            return False