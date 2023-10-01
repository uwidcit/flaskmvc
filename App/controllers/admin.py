from flask import request, jsonify
from App import app, db
from App.models.admin import Admin
from App.models.programme import Program

# Controller for adding a program for the admin.
@app.route('/admin/program', methods=['POST'])
def add_program():
    if not request.is_json:
        return jsonify({"message": "Request is not in JSON format"}), 400

    name = request.json.get('name')

    if not name:
        return jsonify({"message": "Program name is required"}), 400

    new_program = Program(name)

    db.session.add(new_program)
    db.session.commit()

    return jsonify({"message": "Program added successfully"})

# Controller for removing a program for the admin.
@app.route('/admin/program/<int:id>', methods=['DELETE'])
def remove_program(id):
    program = Program.query.get(id)

    if not program:
        return jsonify({"message": "Program not found"}), 404

    db.session.delete(program)
    db.session.commit()

    return jsonify({"message": "Program deleted successfully"})
