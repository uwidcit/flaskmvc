from App.database import db 
from App.models import Student
from App.models import CoursePlan
from App.models import Program
from App.models import Course
from App.models import OfferedCourses



def create_easy_plan(studentId):
    # Get the student object based on studentId
    student = Student.query.get(studentId)
    # Generate a list of courses using the easyCourses function
    courses = easyCourses(student)
    
    # Create a new CoursePlan for the student with the generated courses
    new_course_plan = CoursePlan(studentId=studentId, courses=courses)
    
    # Add the new course plan to the database and commit the changes
    db.session.add(new_course_plan)
    db.session.commit()
    
    return new_course_plan


def addCourse(Student, courseCode):
    plan=CoursePlan.query.filter_by(studentId=Student.id).first()
    plan.courses.append(courseCode)
    print(f'Course added')

def removeCourse(Student, courseCode):
    plan=CoursePlan.query.filter_by(studentId=Student.id).first()
    if courseCode in plan.courses:
        plan.courses.remove(courseCode)
        print(f'Course removed')
        return
    print(f'Course not found')

def getProgramme(Student):
    return Program.query.filter_by(id=Student.program_id).first()

def getRemainingCourses(completed, required):
    # Check if either 'completed' or 'required' is None
    if completed is None or required is None:
        return []  # Return an empty list or handle it in a way that makes sense for your application

    remaining = required.copy()
    for course in required:
        if course in completed:
            remaining.remove(course)
    return remaining


def getRemainingCore(Student):
    programme=getProgramme(Student)
    reqCore=Program.get_core_courses()
    remaining=getRemainingCourses(Student.course_history,reqCore)
    return remaining

def getRemainingFoun(Student):
    programme=getProgramme(Student)
    reqFoun=Program.get_foun_courses()
    remaining=getRemainingCourses(Student.course_history,reqFoun)
    return remaining
def getRemainingElec(Student):
    program = getProgramme(Student)  # Get the student's program
    if program:
        reqElec = program.str_elective_courses()  # Use the instance method to get elective courses
        if reqElec:
            remaining = getRemainingCourses(Student.course_history, reqElec)
            return remaining
    return []

def remElecCredits(Student):
    program = getProgramme(Student)  # Get the student's program
    if program:
        requiredCreds = program.elective_credits  # Access the elective_credits attribute
        elective_courses = program.str_elective_courses()  # Use the instance method to get elective courses
        if elective_courses:
            for course in elective_courses:
                if course in Student.course_history:
                    c = Course.query.filter_by(courseCode=course).first()  # Get course
                    if c:
                        requiredCreds = requiredCreds - c.credits  # Subtract credits
            return requiredCreds
    return 0


def findAvailable(courseList):
    listing=  get_all_courses() #FIX - courses offered (posted by staff)
    available=[]
    for course in courseList:
        if course in listing:
            c=Course.query.filter_by(courseCode=course).first()     #get course
            if c:
                available.append(c)
    return available        #returns an array of course objects


def prioritizeElectives(Student):
    #get available electives
    electives=findAvailable(getRemainingElec(Student))      
    credits=remElecCredits(Student)
    courses=[]
    
    #select courses to satisfy the programme's credit requiremen
    for c in electives:     
        if credits>0:
            courses.append(c)
            credits=credits-c.credits
    
    #merge available, required core and foundation courses
    courses=courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    return courses


def easyCourses(Student):
    #get electives, order by difficulty
    electives=findAvailable(getRemainingElec(Student))      
    electives.sort(key=lambda x:getattr(x, "rating", 0)) 
     
    #select courses to satisfy the programme's credit requirement
    credits=remElecCredits(Student)
    courses=[]
    for c in electives:    
        if credits>0:
            courses.append(c)
            credits=credits-c.credits

    #merge available core and foundation courses and sort by difficulty
    courses= courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    courses.sort(key=lambda x:getattr(x, "rating", 0)) 
    return courses


def fastestGraduation(Student):
    #get electives, order by credits (descending order)
    electives=findAvailable(getRemainingElec(Student))      
    electives.sort(key=lambda x:getattr(x, "credits", 0), reverse=True)

    #select courses to satisfy the programme's credit requirement
    credits=remElecCredits(Student)
    courses=[]
    for c in electives:    
        if credits>0:
            courses.append(c)
            credits=credits-c.credits

    #get available, required core and foundation courses
    courses= courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    return courses