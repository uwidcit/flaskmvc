from App.models import Course, Prerequisites
from App.controllers.prerequistes import (create_prereq, get_all_prerequisites)
from App.database import db
import json, csv

def createPrerequistes(prereqs, courseName):
    for prereq_code in prereqs:
        prereq_course = Course.query.filter_by(courseCode=prereq_code).first()
        
        if prereq_course:
            create_prereq(prereq_code,courseName) 

def create_course(code, name, rating, credits, prereqs):
    already = get_course_by_courseCode(code)
    if already is None:
        course = Course(code, name, rating, credits)

        if prereqs:
            createPrerequistes(prereqs, name)
            
        db.session.add(course)
        db.session.commit()
        return course
    else:
        return None


def createCoursesfromFile(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                courseCode = row["courseCode"]
                courseName = row["courseName"]
                credits = int(row["numCredits"])
                rating = int(row["rating"])
                prerequisites_codes = row["preReqs"].split(',')

                create_course(courseCode, courseName, rating, credits, prerequisites_codes)
                
    except FileNotFoundError:
        print("File not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    print("Courses added successfully.")
    
def get_course_by_courseCode(code):
    return Course.query.filter_by(courseCode=code).first()

def courses_Sorted_byRating():
    courses =  Course.query.order_by(Course.rating.asc()).all()
    codes = []

    for c in courses:
        codes.append(c.courseCode)
    
    return codes

def courses_Sorted_byRating_Objects():
    return Course.query.order_by(Course.rating.asc()).all()
    

def get_prerequisites(code):
    course = get_course_by_courseCode(code)
    prereqs = get_all_prerequisites(course.courseName)
    return prereqs

def get_credits(code):
    course = get_course_by_courseCode(code)
    return course.credits if course else 0

def get_ratings(code):
    course = get_course_by_courseCode(code)
    return course.rating if course else 0



