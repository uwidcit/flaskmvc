from App.models import CoursePlan
from App.database import db 
from App.controllers import (
    get_program_by_id, 
    get_course_by_courseCode, 
    get_credits, 
    getPrereqCodes,
    getCompletedCourses,
    createPlanCourse,
    deleteCourseFromCoursePlan,
    get_allCore,
    get_allFoun,
    get_allElectives,
    getCompletedCourseCodes,
    convertToList,
    get_all_OfferedCodes,
    isCourseOffered
)


def create_CoursePlan(id):
    plan = CoursePlan(id)
    db.session.add(plan)
    db.session.commit()
    return plan

def getCoursePlan(studentid):
    return CoursePlan.query.filter_by(studentId=studentid).first()

def possessPrereqs(Student, course):
    preqs = getPrereqCodes(course.courseName)
    completed = getCompletedCourseCodes(Student.id)
    for course in preqs:
        if course not in completed:
            return False
    
    return True

def addCourseToPlan(Student, courseCode):
    course = get_course_by_courseCode(courseCode)
    if course:
        offered = isCourseOffered(courseCode)
        if offered:
            haveAllpreqs = possessPrereqs(Student, course)
            if haveAllpreqs:
                plan = getCoursePlan(Student.id)
                if plan:
                    createPlanCourse(plan.planId, courseCode)
                    print("Course successfully added to course plan")
                else:
                    plan = create_CoursePlan(Student.id)
                    createPlanCourse(plan.planId, courseCode)
                    print("Plan successfully created and Course was successfully added to course plan")
        else:
            print("Course is not offered")
    else:
        print("Course does not exist")


def removeCourse(Student, courseCode):
    plan=getCoursePlan(Student.id)
    if plan:
        deleteCourseFromCoursePlan(plan.planid, courseCode)

def getRemainingCourses(completed, required):
    # Check if either 'completed' or 'required' is None
    if completed is None or required is None:
        return []  # Return an empty list or handle it in a way that makes sense for your application
    
    completedCodes = []
    for c in completed:
        completedCodes.append(c.code)
    
    remainingCodes = []
    for r in required:
        remainingCodes.append(r.code)

    for a in remainingCodes:
        # print(a)
        if a in completedCodes:
            # print(a)
            remainingCodes.remove(a)

    return remainingCodes


def getRemainingCore(Student):
    programme=get_program_by_id(Student.program_id)
    remaining = []

    if programme:
        reqCore=get_allCore(programme.name)
        completed = getCompletedCourses(Student.id)
        remaining=getRemainingCourses(completed,reqCore)
    
    return remaining


def getRemainingFoun(Student):
    programme = get_program_by_id(Student.program_id)
    remaining =[]

    if programme:
        reqFoun = get_allFoun(programme.name)
        completed = getCompletedCourses(Student.id)
        remaining=getRemainingCourses(completed,reqFoun)
    
    return remaining


def getRemainingElec(Student):
    programme = get_program_by_id(Student.program_id)  # Get the student's program
    remaining = []

    if programme:
        reqElec = get_allElectives(programme.name)  # Use the instance method to get elective courses
        completed = getCompletedCourses(Student.id)
        remaining = getRemainingCourses(completed, reqElec)
            
    return remaining


def remElecCredits(Student):
    programme = get_program_by_id(Student.program_id)  # Get the student's program
    completedcourses = getCompletedCourseCodes(Student.id)
    requiredCreds = 0

    if programme:
        requiredCreds = programme.elective_credits  # Access the elective_credits attribute
        elective_courses = get_allElectives(programme.name)  # Use the instance method to get elective courses
        electCodes = convertToList(elective_courses)
        if electCodes:
            for code in electCodes:
                if code in completedcourses:
                    c = get_course_by_courseCode(code)  # Get course
                    if c:
                        requiredCreds = requiredCreds - c.credits  # Subtract credits
            
    return requiredCreds


def findAvailable(courseList):
    listing=get_all_OfferedCodes()
    available=[]

    for code in courseList:
        if code in listing:
            available.append(code)

    return available        #returns an array of course objects


def checkPrereq(Student, recommnded):
    validCourses=[]
    for course in recommnded:
        c = get_course_by_courseCode(course)
        satisfied = possessPrereqs(Student, c)
        if satisfied:
            validCourses.append(c.courseCode)
    
    return validCourses

def getTopfive(list):
    return list[:5]



def prioritizeElectives(Student):
    #get available electives
    electives=findAvailable(getRemainingElec(Student))      
    credits=remElecCredits(Student)
    courses=[]
    
    #select courses to satisfy the programme's credit requirements
    for c in electives:     
        if credits>0:
            courses.append(c)
            credits = credits - get_credits(c)
    
    #merge available, required core and foundation courses
    courses = courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    courses = checkPrereq(Student,courses)

    for c in courses:
        print(c)
    
    return getTopfive(courses)


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
    updateCoursePlan(Student.id,courses)
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
    # courses= courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))
    courses=checkPrereq(Student,courses)
    return courses

def generator(Student, command):
    courses = []

    if command == "electives":
        plan = create_CoursePlan(Student.id)
        courses = prioritizeElectives(Student)

        for c in courses:
            createPlanCourse(plan.planId, c)


    return courses