from pydantic import BaseModel
from typing import Optional, List

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

class DepartmentResponse(BaseModel):
    id: int
    name: str
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True
