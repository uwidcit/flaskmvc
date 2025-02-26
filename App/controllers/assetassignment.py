from App.models import AssetAssignment
from App.database import db

def create_asset_assignment(assignment_id, asset_id, assigned_to_assignee_id, floor_id, assignment_date=None, return_date=None):
    new_assignment = AssetAssignment(
        assignment_id=assignment_id,
        asset_id=asset_id,
        assigned_to_assignee_id=assigned_to_assignee_id,
        floor_id=floor_id,
        assignment_date=assignment_date,
        return_date=return_date
    )
    db.session.add(new_assignment)
    db.session.commit()
    return new_assignment

def get_asset_assignment_by_id(assignment_id):
    return AssetAssignment.query.get(assignment_id)

def get_all_asset_assignments():
    return AssetAssignment.query.all()

def get_all_asset_assignments_json():
    return [assignment.to_dict() for assignment in get_all_asset_assignments()]

def update_asset_assignment(assignment_id, asset_id=None, assigned_to_assignee_id=None, floor_id=None, assignment_date=None, return_date=None):
    assignment = get_asset_assignment_by_id(assignment_id)
    if assignment:
        if asset_id:
            assignment.asset_id = asset_id
        if assigned_to_assignee_id:
            assignment.assigned_to_assignee_id = assigned_to_assignee_id
        if floor_id:
            assignment.floor_id = floor_id
        if assignment_date:
            assignment.assignment_date = assignment_date
        if return_date is not None:
            assignment.return_date = return_date
        db.session.commit()
        return assignment
    return None

def delete_asset_assignment(assignment_id):
    assignment = get_asset_assignment_by_id(assignment_id)
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
        return True
    return False

