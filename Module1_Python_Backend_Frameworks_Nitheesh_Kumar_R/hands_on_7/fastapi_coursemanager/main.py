from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

import models
import schemas
from database import engine, get_db, Base

app = FastAPI(
    title='Course Management API',
    description='API for managing courses, students, and enrollments',
    version='1.0',
    contact={'name': 'Dev Team', 'email': 'dev@example.com'}
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/', tags=['Root'])
async def root():
    return {'message': 'API running'}

# --- COURSES ---

@app.post('/api/courses/', response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'], summary="Create a new course", response_description="The created course object")
async def create_course(course: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@app.get('/api/courses/', response_model=List[schemas.CourseResponse], tags=['Courses'])
async def get_courses(skip: int = 0, limit: int = 10, department_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(models.Course).offset(skip).limit(limit)
    if department_id is not None:
        query = query.filter(models.Course.department_id == department_id)
    
    result = await db.execute(query)
    return result.scalars().all()

@app.get('/api/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put('/api/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course_update: schemas.CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    
    await db.commit()
    await db.refresh(course)
    return course

@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    await db.delete(course)
    await db.commit()
    return None

@app.get('/api/courses/{course_id}/students/', response_model=List[schemas.StudentResponse], tags=['Courses'])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    if course.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Course not found")
        
    query = select(models.Student).join(models.Enrollment).filter(models.Enrollment.course_id == course_id)
    result = await db.execute(query)
    return result.scalars().all()

# --- STUDENTS ---
@app.post('/api/students/', response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

@app.get('/api/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put('/api/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'])
async def update_student(student_id: int, student_update: schemas.StudentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    await db.commit()
    await db.refresh(student)
    return student

@app.delete('/api/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    await db.delete(student)
    await db.commit()
    return None

# --- ENROLLMENTS ---
def send_confirmation_email(student_email: str):
    print(f'Sending confirmation to {student_email}')

@app.post('/api/enrollments/', response_model=schemas.EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
async def create_enrollment(enrollment: schemas.EnrollmentCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    
    # Get student to fetch email
    student_res = await db.execute(select(models.Student).filter(models.Student.id == enrollment.student_id))
    student = student_res.scalar_one_or_none()
    if student and student.email:
        background_tasks.add_task(send_confirmation_email, student.email)
        
    return db_enrollment

@app.get('/api/enrollments/{enrollment_id}', response_model=schemas.EnrollmentResponse, tags=['Enrollments'])
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).filter(models.Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment

@app.delete('/api/enrollments/{enrollment_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Enrollments'])
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).filter(models.Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    await db.delete(enrollment)
    await db.commit()
    return None
