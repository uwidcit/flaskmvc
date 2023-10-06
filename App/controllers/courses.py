from App.models import Course, Prerequisites
from App.controllers.prerequistes import (create_prereq, get_all_prerequisites)
from App.database import db
import json, csv

def create_course(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                course = Course()
                course.courseCode = row["courseCode"]
                course.courseName = row["courseName"]
                course.credits = int(row["numCredits"])
                course.rating = int(row["rating"])
                prerequisites_codes = row["preReqs"].split(',')
                
                if prerequisites_codes[0]:
                    prerequisites = []
                    for prereq_code in prerequisites_codes:
                        prereq_course = Course.query.filter_by(courseCode=prereq_code).first()
                        
                        if prereq_course:
                            create_prereq(prereq_code, course.courseName) 
                db.session.add(course)
                
    except FileNotFoundError:
        print("File not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    db.session.commit()
    print("Courses added successfully.")
    
def get_course_by_courseCode(code):
    return Course.query.filter_by(courseCode=code).first()

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

