from App.models import User 
from App.models import Student
from App.models import Staff 
from App.models import Admin
from App.database import db
from App.controllers import create_user
from App.controllers.staff import create_staff


def createAdmin(id, username, password, name):
  newadmin = Admin(id, username, password, name)
  try:
    db.session.add(newadmin)
    db.session.commit()
  except Exception as e:  #admin already exists
    db.session.rollback()
    print(f'Username already taken')
  print(f'Admin created.')
  return newadmin


# def addStudent(id,username,password):       #creates new student
#     newstudent=Student(id=id,username=username,password=password) 
#     try:
#         db.session.add(newstudent)
#         db.session.commit()
#     except Exception as e:      #student already exists
#         db.session.rollback()
#         print(f'Username or ID already taken')
#     print(f'Student created.')
#     return newstudent


def addStaff(id,username,password,name):     #creates new staff member
    newstaff = create_staff(password, id, name)
    return newstaff


def removeAccount(id):      #removes account by id
    acc=User.query.filter_by(id=id).first()
    if not acc:
        print(f'Account with ID {id} not found.')
        return
    student=Student.query.filter_by(id=id).first()
    staff=Staff.query.filter_by(id=id).first()
    if student:
        db.session.delete(student)
    else:
        db.session.delete(staff)
    db.session.delete(acc)
    db.session.commit()
    print(f'Account deleted.')
