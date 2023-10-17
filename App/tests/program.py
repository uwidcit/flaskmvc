import unittest
from App.models import Program

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
