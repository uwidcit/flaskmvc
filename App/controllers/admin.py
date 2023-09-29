from App.models import User 
from App.models import Student
from App.models import Staff 
from App.models import db

def addStudent(id,username,password):       #creates new student
    newstudent=Student(id=id,username=username,password=password) 
    try:
        db.session.add(newstudent)
        db.session.commit()
    except Exception as e:      #student already exists
        db.session.rollback()
        print(f'Username or ID already taken')
    print(f'Student created.')
    return newstudent

def addStaff(id,username,password):     #creates new staff member
    newstaff=Staff(id=id,username=username,password=password)
    try:
        db.session.add(newstaff)
        db.session.commit()
    except Exception as e:      #staff already exists
        db.session.rollback()
        print(f'Username or ID already taken')
    print(f'Staff created.')
    return newstaff

def removeAccount(id):      #removes account by id
    acc=User.query.filter_by(id=id).first()
    if not acc:
        print(f'Account with ID {id} not found.')
        return
    db.session.delete(acc)
    db.session.commit()
    print(f'Account deleted.')
