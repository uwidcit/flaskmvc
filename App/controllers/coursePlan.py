from App.database import db 
#from App.models import Student
from App.models import CoursePlan
from App.models import Program
from App.models import Course
from App.models import OfferedCourses

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
    return Program.query.filter_by(programmeId=Student.programme_id).first()

def getRemainingCourses(completed, required):
    remaining=required.copy()
    for course in required:
        if course in completed:
            remaining.remove(course)
    return remaining

def getRemainingCore(Student):
    programme=getProgramme(Student)
    reqCore=Program.get_core_courses()
    remaining=getRemainingCourses(Student.courseHistory,reqCore)
    return remaining

def getRemainingFoun(Student):
    programme=getProgramme(Student)
    reqFoun=Program.get_foun_courses()
    remaining=getRemainingCourses(Student.courseHistory,reqFoun)
    return remaining

def getRemainingElec(Student):
    programme=getProgramme(Student)
    reqElec=Program.get_elective_courses()
    remaining=getRemainingCourses(Student.courseHistory,reqElec)
    return remaining

def remElecCredits(Student):
    programme=getProgramme(Student)
    requiredCreds=Program.get_elective_credits
    for course in programme.elective_courses:
        if course in Student.courseHistory:
            c=Course.query.filter_by(courseCode=course).first()     #get course
            requiredCreds=requiredCreds-c.credits     #subtract credits
    return requiredCreds

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