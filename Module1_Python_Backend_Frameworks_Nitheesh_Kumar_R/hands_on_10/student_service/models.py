from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

    def __init__(self, first_name, last_name, email, **kwargs):
        super().__init__(first_name=first_name, last_name=last_name, email=email, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False) # Only holds the ID of the course from course_service

    def __init__(self, student_id, course_id, **kwargs):
        super().__init__(student_id=student_id, course_id=course_id, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id
        }
