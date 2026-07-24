from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

import models
import schemas
from database import engine, get_db, Base

app = FastAPI(title='Course Management API', version='1.0')

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/')
async def root():
    return {'message': 'API running'}

@app.post('/api/courses/', response_model=schemas.CourseResponse, status_code=201)
async def create_course(course: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

@app.get('/api/courses/', response_model=List[schemas.CourseResponse])
async def get_courses(skip: int = 0, limit: int = 10, department_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(models.Course).offset(skip).limit(limit)
    if department_id is not None:
        query = query.filter(models.Course.department_id == department_id)
    
    result = await db.execute(query)
    courses = result.scalars().all()
    return courses

@app.get('/api/courses/{course_id}', response_model=schemas.CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
