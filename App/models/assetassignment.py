from App.database import db
from datetime import datetime

class AsserAssignment(db.Model):
    assignment_id = db.Column(db.String(50), primary_key=True)
    asset_id = db.Column(db.String(50), db.ForeignKey('asset.asset_id'), nullable=False)
    assigned_to_assignee_id = db.Column(db.String(50), db.ForeignKey('assignee.assignee.id'), nullable=False)
    floor_id = db.Column(db.String(50), db.ForeignKey('floor.floor_id'), nullable=False)
    assignment_date = db.Column(
        db.String(50), nullable=False, default=lambda: datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    )
    return_date = db.Column(db.String(50), nullable=True)

    def __init__(self, assignment_id, asset_id, assigned_to_assignee_id, floor_id, assignment_date=None, return_date=None):
        self.assignment_id = assignment_id
        self.asset_id = asset_id
        self.assigned_to_assignee_id = assigned_to_assignee_id
        self.floor_id = floor_id
        self.assignment_date = assignment_date if assignment_date else datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.return_date = return_date

    def get_json(self):
        return {
            'assignment_id': self.assignment_id,
            'asset_id': self.asset_id,
            'assigned_to_assignee_id': self.assigned_to_assignee_id,
            'floor_id': self.floor_id,
            'assignment_date': self.assignment_date,
            'return_date': self.return_date
        }
    
    def __repr__(self):
        return f"<AssetAssignment {self.assignment_id}>"
    
    def __str__(self):
        return f'Assignment {self.assignment_id} (Asset: {self.asset_id}, Assignee: {self.assigned_to_assignee_id}, Floor: {self.floor_id})'
    