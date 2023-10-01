from App.database import db 
from App.models import Student
from App.models import CoursePlan
from App.models import Program
from App.models import Course

def addCourse(Student, courseCode):
    plan=CoursePlan.query.filter_by(studentId=Student.id).first()
    #verify prereqs
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
    return Program.query.filter_by(programmeId=Student.programme_id).first()

def getRemainingCourses(completed, required):
    remaining=required.copy()
    for course in required:
        if course in completed:
            remaining.remove(course)
    return remaining

def getRemainingCore(Student):
    programme=getProgramme(Student)
    reqCore=programme.get_core_courses(programme.name)
    remaining=getRemainingCourses(Student.courseHistory,reqCore)
    return remaining

def getRemainingFoun(Student):
    programme=getProgramme(Student)
    reqFoun=programme.get_foun_courses(programme.name)
    remaining=getRemainingCourses(Student.courseHistory,reqFoun)
    return remaining

def getRemainingElec(Student):
    programme=getProgramme(Student)
    reqElec=programme.get_elective_courses(programme.name)
    remaining=getRemainingCourses(Student.courseHistory,reqElec)
    return remaining

def remElecCredits(Student):
    programme=getProgramme(Student)
    requiredCreds=programme.get_elective_credits(programme.name)
    for course in programme.get_elective_courses(programme.name):
        if course in Student.courseHistory:
            c=Course.query.filter_by(courseCode=course).first()     #get course
            requiredCreds=requiredCreds-c.get_credits(course)     #subtract credits
    return requiredCreds

def findAvailable(courseList):
    listing=[]   #FIX - courses offered (posted by staff)
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
            credits=credits-c.credits
    
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
            credits=credits-c.credits

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
            credits=credits-c.credits

    #get available, required core and foundation courses
    courses= courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    courses=checkPrereq(Student,courses)
    return courses