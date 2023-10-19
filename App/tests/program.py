import unittest, pytest
from App.models import Program
from App.main import create_app
from App.database import db, create_db
from App.controllers import create_program, get_program_by_name

class ProgramUnitTests(unittest.TestCase):

    def test_new_program(self):
        programname = "Information Technology Special"
        core_credits = 69
        elective_credits = 15
        foun_credits = 9
        program = Program(programname, core_credits, elective_credits, foun_credits)
        self.assertEqual(program.name, programname)
        self.assertEqual(program.core_credits, core_credits)
        self.assertEqual(program.elective_credits, elective_credits)
        self.assertEqual(program.foun_credits, foun_credits)
    
    def test_program_toJSON(self):
        programname = "Information Technology Special"
        core_credits = 69
        elective_credits = 15
        foun_credits = 9
        
        program = Program(programname, core_credits, elective_credits, foun_credits)
        program_json = program.get_json()

        self.assertDictEqual(program_json, {
            'Program ID:': None,
            'Program Name: ': programname,
            'Core Credits: ': core_credits,
            'Elective Credits ': elective_credits,
            'Foundation Credits: ': foun_credits,
        })

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class ProgramIntegrationTests(unittest.TestCase):
    def test_create_program(self):
        program = create_program("IT", 69, 15, 9)
        assert get_program_by_name("IT") != None