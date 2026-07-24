from app import create_app
from extensions import db
from courses.models import Department, Course, Student, Enrollment

app = create_app()
with app.app_context():
    # Check if DB is already seeded
    if Course.query.first():
        print("Database is already seeded!")
        import sys
        sys.exit(0)

    # Insert 2 departments
    dept1 = Department(name="Computer Science", head_of_dept="Alan Turing", budget=50000)
    dept2 = Department(name="Mathematics", head_of_dept="John Nash", budget=30000)
    db.session.add_all([dept1, dept2])
    db.session.commit()

    # Insert 3 courses
    c1 = Course(name="Intro to Programming", code="CS101", credits=3, department_id=dept1.id)
    c2 = Course(name="Data Structures", code="CS201", credits=4, department_id=dept1.id)
    c3 = Course(name="Calculus I", code="MATH101", credits=4, department_id=dept2.id)
    db.session.add_all([c1, c2, c3])
    db.session.commit()

    # Create students and enrollments to test /students/ join endpoint
    s1 = Student(first_name="Alice", last_name="Smith", email="alice@college.edu", enrollment_year=2023, department_id=dept1.id)
    s2 = Student(first_name="Bob", last_name="Jones", email="bob@college.edu", enrollment_year=2023, department_id=dept1.id)
    db.session.add_all([s1, s2])
    db.session.commit()

    e1 = Enrollment(student_id=s1.id, course_id=c1.id, grade="A")
    e2 = Enrollment(student_id=s2.id, course_id=c1.id, grade="B")
    db.session.add_all([e1, e2])
    db.session.commit()

    print("Inserted courses:")
    courses = Course.query.all()
    for c in courses:
        print(f"- {c.name} ({c.code})")
