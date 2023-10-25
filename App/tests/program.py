import unittest, pytest
from App.models import Program, ProgramCourses
from App.main import create_app
from App.database import db, create_db
from App.controllers import create_program, get_program_by_name,create_course, create_programCourse, get_all_programCourses, programCourses_SortedbyRating,programCourses_SortedbyHighestCredits

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

    def test_new_program_course(self):
        programcourse=ProgramCourses("1","INFO2605","2")
        assert programcourse.code=="INFO2605"

    def test_program_course_toJSON(self):
        programcourse=ProgramCourses("1","INFO2605","2")
        programcourse_json=programcourse.get_json()
        self.assertDictEqual(programcourse_json,{'Program Course ID:':None, 'Program ID:':'1','Course Code: ':'INFO2605','Course Type: ':'2'})




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

    def test_create_program_requirement(self):
        create_course("MATH1115", "Fundamental Mathematics for the General Sciences 1",1,6,[])
        create_course("MATH2250", "Industrial Statistics",4,3,[])
        create_course("INFO2606", "Internship",1,6,[])

        create_programCourse("IT","MATH1115",1)
        program_courses=get_all_programCourses("IT")
        assert any(course.code == "MATH1115" for course in program_courses)

    def test_programCourses_sorted_by_credits(self):        
        create_programCourse("IT","INFO2606",2)
        program=get_program_by_name("IT")
        credits_sorted=programCourses_SortedbyHighestCredits(program.id)
        self.assertListEqual(credits_sorted,['INFO2606', 'MATH1115'])   

    def test_programCourses_sorted_by_rating(self):
        create_programCourse("IT","MATH2250",1)
        program=get_program_by_name("IT")
        rating_list=programCourses_SortedbyRating(program.id)
        self.assertListEqual(rating_list,['MATH1115', 'INFO2606', 'MATH2250'])