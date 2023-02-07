from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(120), nullable=True)
    image_url = db.Column(db.String(120), nullable=True)
    institution = db.Column(db.String(120), nullable=False)
    faculty = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    researcher_sub_records = db.relationship("ResearcherSubRecord", foreign_keys='ResearcherSubRecord.user_id', backref="subscriber", lazy=True, cascade="all, delete-orphan")
    topic_sub_records = db.relationship("TopicSubRecord", backref="subscriber", lazy=True, cascade="all, delete-orphan")
    notification_records = db.relationship("NotificationRecord", backref="user", lazy=True, cascade="all, delete-orphan")

    def __init__(self):
        pass

    # def __init__(self, email, password, first_name, middle_name, last_name, institution, faculty, department, image_url):
    #     self.email = email
    #     self.set_password(password)
    #     self.first_name = first_name
    #     self.middle_name = middle_name
    #     self.last_name = last_name
    #     self.institution = institution
    #     self.faculty = faculty
    #     self.department = department
    #     self.image_url = image_url

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def toDict(self):
        return{
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'institution': self.institution,
            'faculty': self.faculty,
            'department': self.department,
            'image_url': self.image_url
        }