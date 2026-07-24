from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedCourseResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[CourseResponse]

class DepartmentResponse(BaseModel):
    id: int
    name: str
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    enrollment_year: int
    department_id: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    enrollment_year: Optional[int] = None
    department_id: Optional[int] = None

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    grade: Optional[str] = None

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    grade: Optional[str] = None

class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True
