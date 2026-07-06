"""
Task 3 Comparison

Without joinedload:
-------------------
1 query for enrollments
+ N queries for students
+ N queries for courses

Example:
4 enrollments
= 1 + 4 + 4 = 9 queries (or more)

With joinedload():
------------------
Only ONE SQL query is executed using JOINs.

This eliminates the N+1 problem.
"""

from sqlalchemy.orm import sessionmaker, joinedload

from models import (
    engine,
    Department,
    Student,
    Course,
    Enrollment,
)

Session = sessionmaker(bind=engine)
session = Session()

# ------------------------------------------------
# INSERT Departments
# ------------------------------------------------

cs = Department(dept_name="Computer Science")
it = Department(dept_name="Information Technology")
ece = Department(dept_name="Electronics")

session.add_all([cs, it, ece])
session.commit()

# ------------------------------------------------
# INSERT Students
# ------------------------------------------------

s1 = Student(
    student_name="Rahul",
    email="rahul@gmail.com",
    enrollment_year=2022,
    department=cs,
)

s2 = Student(
    student_name="Anjali",
    email="anjali@gmail.com",
    enrollment_year=2023,
    department=cs,
)

s3 = Student(
    student_name="Vijay",
    email="vijay@gmail.com",
    enrollment_year=2021,
    department=it,
)

s4 = Student(
    student_name="Sneha",
    email="sneha@gmail.com",
    enrollment_year=2022,
    department=ece,
)

s5 = Student(
    student_name="Amit",
    email="amit@gmail.com",
    enrollment_year=2023,
    department=cs,
)

session.add_all([s1, s2, s3, s4, s5])
session.commit()

# ------------------------------------------------
# INSERT Courses
# ------------------------------------------------

c1 = Course(course_name="Database Systems", credits=4)
c2 = Course(course_name="Python Programming", credits=3)
c3 = Course(course_name="Operating Systems", credits=4)

session.add_all([c1, c2, c3])
session.commit()

# ------------------------------------------------
# INSERT Enrollments
# ------------------------------------------------

e1 = Enrollment(student=s1, course=c1)
e2 = Enrollment(student=s2, course=c2)
e3 = Enrollment(student=s3, course=c3)
e4 = Enrollment(student=s5, course=c1)

session.add_all([e1, e2, e3, e4])
session.commit()

print("\nDepartments, Students, Courses and Enrollments inserted.\n")

# ------------------------------------------------
# READ
# Students in Computer Science
# ------------------------------------------------

print("Students in Computer Science Department")

students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == "Computer Science")
    .all()
)

for student in students:
    print(student.student_name)

# ------------------------------------------------
# READ (N+1)
# ------------------------------------------------

print("\nEnrollment Details (Without joinedload)\n")

enrollments = session.query(Enrollment).all()

for e in enrollments:
    print(e.student.student_name, "->", e.course.course_name)

# ------------------------------------------------
# UPDATE
# ------------------------------------------------

student = (
    session.query(Student)
    .filter(Student.email == "rahul@gmail.com")
    .first()
)

if student:
    student.enrollment_year = 2024
    session.commit()
    print("\nStudent updated successfully.")

# ------------------------------------------------
# DELETE
# ------------------------------------------------

enrollment = session.query(Enrollment).first()

if enrollment:
    session.delete(enrollment)
    session.commit()
    print("Enrollment deleted successfully.")

# ------------------------------------------------
# EAGER LOADING (Fix N+1)
# ------------------------------------------------

print("\nEnrollment Details (Using joinedload)\n")

enrollments = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    )
    .all()
)

for e in enrollments:
    print(e.student.student_name, "->", e.course.course_name)

session.close()

