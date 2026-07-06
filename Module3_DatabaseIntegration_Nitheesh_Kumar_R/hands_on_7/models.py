from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Time,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

# PostgreSQL Connection
DATABASE_URL = "postgresql+psycopg2://postgres:abc%40123@localhost/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


# ---------------- Department ----------------
class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(Integer, primary_key=True)
    dept_name = Column(String(100), nullable=False)

    students = relationship("Student", back_populates="department")
    professors = relationship("Professor", back_populates="department")


# ---------------- Student ----------------
class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    student_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    enrollment_year = Column(Integer)

    # New column
    is_active = Column(Boolean, default=True)

    dept_id = Column(Integer, ForeignKey("departments.dept_id"))

    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")


# ---------------- Professor ----------------
class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(Integer, primary_key=True)
    professor_name = Column(String(100))

    dept_id = Column(Integer, ForeignKey("departments.dept_id"))

    department = relationship("Department", back_populates="professors")


# ---------------- Course ----------------
class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(100))
    credits = Column(Integer)

    enrollments = relationship("Enrollment", back_populates="course")
    schedules = relationship("CourseSchedule", back_populates="course")


# ---------------- Enrollment ----------------
class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey("students.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


# ---------------- Course Schedule ----------------
class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id = Column(Integer, primary_key=True)

    course_id = Column(Integer, ForeignKey("courses.course_id"))

    day_of_week = Column(String(20))
    start_time = Column(Time)
    end_time = Column(Time)

    course = relationship("Course", back_populates="schedules")


# Create Tables
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created successfully.")