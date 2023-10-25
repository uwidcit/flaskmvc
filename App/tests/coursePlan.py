import pytest, unittest
from App.models import CoursePlan, CoursePlanCourses
from App.controllers import create_CoursePlan, create_student, create_program, addCourseToPlan, enroll_in_programme, addSemesterCourses, generator, createCoursesfromFile, get_program_by_name, getCoursePlan, get_all_courses_by_planid, get_student, create_programCourse, removeCourse
from App.main import create_app
from App.database import db, create_db

class CoursePlanUnitTests(unittest.TestCase):
    
    def test_new_courseplan(self):
        student_id = "01234"
        course_plan = CoursePlan(student_id)
        self.assertEqual(course_plan.studentId, student_id)
    
    def test_courseplan_toJSON(self):
        student_id = "01234"
        course_plan = CoursePlan(student_id)
        course_plan_json = course_plan.get_json()
        self.assertDictEqual(course_plan_json, {"planId": None, "studentId": student_id})


    def test_new_courseplan_courses(self):
        student_id = "01234"
        course_plan = CoursePlan(student_id)
        course_code = "INFO2605"
        courseplan_courses = CoursePlanCourses("1", course_code)
        self.assertEqual(courseplan_courses.code, course_code)
       
    

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


# Integration Tests
class CoursePlanIntegrationTests(unittest.TestCase):

    def test_create_course_plan(self):
        # Create a student and program.
        program = create_program("Computer Science Major", 69, 15, 9)
        student = create_student("1234", "johnpass", "John Doe", program.name)

        #Create courses, semester courses and program coursess
        createCoursesfromFile('testData/courseData.csv')

        file_path = "testData/test.txt"
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()
                if i ==0:
                    programName = line
                else:
                    course = line.split(',')
                    create_programCourse(programName, course[0],int(course[1]))

        file_path1='testData/test2.txt'
        with open(file_path1, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()
                addSemesterCourses(line)


        plan = create_CoursePlan(student.id)
        self.assertIsNotNone(plan)
        assert getCoursePlan(student.id) != None
        
        course_code = "INFO1601"
        added_plan = addCourseToPlan(student, course_code)
        courseplan_courses = get_all_courses_by_planid("1")
        
        self.assertIsNotNone(added_plan)
        self.assertIn('INFO1601', [course.code for course in courseplan_courses])
        
    
    def test_remove_course_from_plan(self):
        program = get_program_by_name("Computer Science Major")
        student = get_student("1234")
        plan_id = enroll_in_programme("1234", program.id)
        courseplan_courses = get_all_courses_by_planid(plan_id)
        self.assertIn('INFO1601', [course.code for course in courseplan_courses])
        removeCourse(student, "INFO1601")
        courseplan_courses = get_all_courses_by_planid(plan_id)
        self.assertNotIn('INFO1601', [course.code for course in courseplan_courses])


    def test_create_fastGraduation_course_plan(self):
        program = get_program_by_name("Computer Science Major")
        student = get_student("1234")
        plan_id = enroll_in_programme("1234", program.id)
        
        courseplan_courses = get_all_courses_by_planid(plan_id)
        course_codes = [course.code for course in courseplan_courses]
        for course_code in course_codes:
            removeCourse(student, course_code)

        generator(student, "fastest")
        courseplan_courses = get_all_courses_by_planid(plan_id)

        print("Courses in Course Plan:")
        for course in courseplan_courses:
            print(course.code)

        self.assertIsNotNone(courseplan_courses)
        self.assertIn('COMP1601', [course.code for course in courseplan_courses])
        

    def test_create_easy_course_plan(self):
        program = get_program_by_name("Computer Science Major")
        student = get_student("1234")
        plan_id = enroll_in_programme("1234", program.id)

        courseplan_courses = get_all_courses_by_planid(plan_id)
        course_codes = [course.code for course in courseplan_courses]
        for course_code in course_codes:
            removeCourse(student, course_code)

        # Create a easy graduation course plan
        generator(student, "easy")
        courseplan_courses = get_all_courses_by_planid(plan_id)

        self.assertIsNotNone(courseplan_courses)
        self.assertIn('COMP1601', [course.code for course in courseplan_courses])
        
    def test_create_electives_course_plan(self):
        program = get_program_by_name("Computer Science Major")
        student = get_student("1234")
        plan_id = enroll_in_programme("1234", program.id)

        courseplan_courses = get_all_courses_by_planid(plan_id)
        course_codes = [course.code for course in courseplan_courses]
        for course_code in course_codes:
            removeCourse(student, course_code)

        # Create an electives graduation course plan
        generator(student, "electives")
        courseplan_courses = get_all_courses_by_planid(plan_id)

        self.assertIsNotNone(courseplan_courses)
        self.assertIn('COMP1601', [course.code for course in courseplan_courses])
        
    def test_get_course_plan_json(self):
        
        program = get_program_by_name("Computer Science Major")
        student = get_student("1234")
        plan_id = enroll_in_programme("1234", program.id)

        courseplan_courses = get_all_courses_by_planid(plan_id)
        course_codes = [course.code for course in courseplan_courses]
        for course_code in course_codes:
            removeCourse(student, course_code)
        
        course_code = "INFO1601"
        added_plan = addCourseToPlan(student, course_code)
        courseplan_courses = get_all_courses_by_planid(plan_id)
        courseplan = getCoursePlan("1234")
        self.assertIsNotNone(added_plan)
        self.assertIn('INFO1601', [course.code for course in courseplan_courses])

        course_plan_json = courseplan.get_json()
        
        expected_json = {
            'planId': 1, 
            'studentId': 1234
        }
        self.assertEqual(course_plan_json, expected_json)


