from App.database import db 
from App.models import Student
from App.models import Staff
from App.models import CoursePlan
from App.models import Program
from App.models import Course
from App.models import OfferedCourses


def getProgramme(Student):
    return Program.query.filter_by(id=Student.program_id).first()


def getOfferedCourses():
    staff=Staff.first()
    return staff.get_all_courses()


def addCourse(Student, courseCode):
    plan=CoursePlan.query.filter_by(studentId=Student.id).first()
    course=checkPrereq(Student,[{courseCode}])    #verify prereqs
    if course:
        validCourse=findAvailable(course)#check availability
    else:
        print(f'Pre-req unsatisfied')
    
    if validCourse:
        plan.courses.append(courseCode)
        print(f'Course added')
    else:
        print(f'Course not available')


def removeCourse(Student, courseCode):
    plan=CoursePlan.query.filter_by(studentId=Student.id).first()
    if courseCode in plan.courses:
        plan.courses.remove(courseCode)
        print(f'Course removed')
        return
    print(f'Course not found')


def getRemainingCourses(completed, required):
    remaining=required.copy()

    # Check if either 'completed' or 'required' is None
    if completed is None or required is None:
        return []  # Return an empty list or handle it in a way that makes sense for your application
    
    for course in required:
        if course in completed:
            remaining.remove(course)
    return remaining


def getRemainingCore(Student):
    programme=getProgramme(Student)
    reqCore=programme.get_core_courses(programme.name)
    remaining=getRemainingCourses(Student.course_history,reqCore)
    return remaining


def getRemainingFoun(Student):
    programme=getProgramme(Student)
    reqFoun=programme.get_foun_courses(programme.name)
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
    listing=getOfferedCourses()
    available=[]
    for course in courseList:
        if course in listing:
            c=Course.query.filter_by(courseCode=course).first()     #get course
            if c:
                available.append(c)
    return available        #returns an array of course objects


def checkPrereq(Student, listing):
    completed=Student.courseHistory
    validCourses=[]

    for course in listing:
        satisfied=True
        prereq=course.get_prerequisites(course.courseCode)
        #check if the student did all the prereq courses
        for c in prereq:
            if c not in completed:      #if at least one was not done, the student can't take the course
                satisfied=False
        if satisfied:
            validCourses.append(c)
    
    return validCourses


def prioritizeElectives(Student):
    #get available electives
    electives=findAvailable(getRemainingElec(Student))      
    credits=remElecCredits(Student)
    courses=[]
    
    #select courses to satisfy the programme's credit requirements
    for c in electives:     
        if credits>0:
            courses.append(c)
            credits=credits-c.get_credits(c.courseCode)
    
    #merge available, required core and foundation courses
    courses=courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    courses=checkPrereq(Student,courses)
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
            credits=credits-c.get_credits(c.courseCode)

    #merge available core and foundation courses and sort by difficulty
    courses= courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    courses.sort(key=lambda x:getattr(x, "rating", 0)) 
    courses=checkPrereq(Student,courses)
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
            credits=credits-c.get_credits(c.courseCode)

    #get available, required core and foundation courses
    courses= courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    courses=checkPrereq(Student,courses)
    return courses

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