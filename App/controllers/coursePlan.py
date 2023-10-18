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
    isCourseOffered,
    programCourses_SortedbyRating,
    programCourses_SortedbyHighestCredits,
    get_all_courses_by_planid,
    
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
                    return plan
                else:
                    plan = create_CoursePlan(Student.id)
                    createPlanCourse(plan.planId, courseCode)
                    print("Plan successfully created and Course was successfully added to course plan")
                    return plan
        else:
            print("Course is not offered")
    else:
        print("Course does not exist")


def removeCourse(Student, courseCode):
    plan=getCoursePlan(Student.id)
    if plan:
        deleteCourseFromCoursePlan(plan.planId, courseCode)

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
    

    notCompleted = remainingCodes.copy()
    for a in completedCodes:
        if a in notCompleted:
            notCompleted.remove(a)

    return notCompleted


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

    return available        #returns an array of course codes


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
    return getTopfive(courses)


def removeCoursesFromList(list1,list2):
    newlist = list2.copy()
    for a in list1:
        if a in newlist:
            newlist.remove(a)
    return newlist
    

def easyCourses(Student):
    program = get_program_by_id(Student.program_id)
    completed = getCompletedCourseCodes(Student.id)
    codesSortedbyRating = programCourses_SortedbyRating(Student.program_id)

    coursesToDo = removeCoursesFromList(completed, codesSortedbyRating)

    elecCredits = remElecCredits(Student)
    
    if elecCredits == 0:
        allElectives = convertToList(get_allElectives(program.name))
        coursesToDo = removeCoursesFromList(allElectives, coursesToDo)
    
    coursesToDo = findAvailable(coursesToDo)

    ableToDo = checkPrereq(Student, coursesToDo)
    # for a in ableToDo:
    #     print(a)
    
    return getTopfive(ableToDo)


def fastestGraduation(Student):
    program = get_program_by_id(Student.program_id)
    sortedCourses = programCourses_SortedbyHighestCredits(Student.program_id)
    completed = getCompletedCourseCodes(Student.id)

    coursesToDo = removeCoursesFromList(completed, sortedCourses)

    elecCredits = remElecCredits(Student)
    
    if elecCredits == 0:
        allElectives = convertToList(get_allElectives(program.name))
        coursesToDo = removeCoursesFromList(allElectives, coursesToDo)
    
    coursesToDo = findAvailable(coursesToDo)
    ableToDo = checkPrereq(Student, coursesToDo)

    return getTopfive(ableToDo)

def commandCall(Student, command):
    courses = []

    if command == "electives":
        courses = prioritizeElectives(Student)
    
    elif command == "easy":
        courses = easyCourses(Student)
    
    elif command == "fastest":
        courses = fastestGraduation(Student)
    
    else:
        print("Invalid command")
    
    return courses


def generator(Student, command):
    courses = []

    plan = getCoursePlan(Student.id)

    if plan is None:
        plan = plan = create_CoursePlan(Student.id)

    
    courses = commandCall(Student, command)

    existingPlanCourses = get_all_courses_by_planid(plan.planId)

    planCourses = []
    for q in existingPlanCourses:
        planCourses.append(q.code)

    for c in courses: 
        if c not in planCourses:
            createPlanCourse(plan.planId, c)

    return courses