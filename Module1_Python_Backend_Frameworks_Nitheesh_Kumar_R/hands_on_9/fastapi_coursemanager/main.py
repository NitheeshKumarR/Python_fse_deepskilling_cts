from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Response, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

import models
import schemas
import security
from database import engine, get_db, Base

SECRET_KEY = "super-secret-key-for-hands-on"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")

"""
# OAuth2 Authorization Code flow vs Simple JWT Login
# The simple JWT login we implemented issues a token directly to the client when they provide credentials.
# The OAuth2 Authorization Code flow involves a third-party authorization server (like Google or GitHub).
# Instead of giving credentials directly to the app, the user authenticates with the Auth Server, which 
# redirects back to the app with a temporary 'Authorization Code'. The app then exchanges this code for 
# an access token. This is much more secure for third-party integrations as the app never sees the password.
"""

app = FastAPI(
    title='Course Management API - Secured',
    description='API for managing courses, students, and enrollments with REST best practices and JWT Auth',
    version='1.0',
    contact={'name': 'Dev Team', 'email': 'dev@example.com'}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    code = 'NOT_FOUND' if exc.status_code == 404 else 'ERROR'
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': {'code': code, 'message': str(exc.detail), 'field': None}}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={'error': {'code': 'UNPROCESSABLE_ENTITY', 'message': 'Validation error', 'field': str(exc.errors())}}
    )

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/', tags=['Root'])
async def root():
    return {'message': 'API running'}

# --- AUTH ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(models.User).filter(models.User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

@app.post('/api/v1/auth/register/', status_code=status.HTTP_201_CREATED, tags=['Auth'])
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "User registered successfully"}

@app.post('/api/v1/auth/login/', response_model=schemas.Token, tags=['Auth'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- COURSES ---

@app.post('/api/v1/courses/', response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'], summary="Create a new course", response_description="The created course object")
async def create_course(course: schemas.CourseCreate, response: Response, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    response.headers['Location'] = f'/api/v1/courses/{db_course.id}/'
    return db_course

@app.get('/api/v1/courses/', response_model=schemas.PaginatedCourseResponse, tags=['Courses'])
async def get_courses(request: Request, page: int = 1, page_size: int = 10, search: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * page_size
    query = select(models.Course)
    count_query = select(func.count()).select_from(models.Course)
    
    if search:
        search_filter = models.Course.name.ilike(f'%{search}%') | models.Course.code.ilike(f'%{search}%')
        query = query.filter(search_filter)
        count_query = count_query.filter(search_filter)

    total = await db.execute(count_query)
    total_count = total.scalar()

    query = query.offset(skip).limit(page_size)
    result = await db.execute(query)
    courses = result.scalars().all()
    
    base_url = str(request.url).split('?')[0]
    next_url = f"{base_url}?page={page+1}&page_size={page_size}" if (skip + page_size) < total_count else None
    prev_url = f"{base_url}?page={page-1}&page_size={page_size}" if page > 1 else None

    return {
        'count': total_count,
        'next': next_url,
        'previous': prev_url,
        'results': courses
    }

@app.get('/api/v1/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    return course

@app.put('/api/v1/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course_update: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    
    update_data = course_update.model_dump()
    for key, value in update_data.items():
        setattr(course, key, value)
    
    await db.commit()
    await db.refresh(course)
    return course

@app.patch('/api/v1/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
async def patch_course(course_id: int, course_update: schemas.CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    
    update_data = course_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    
    await db.commit()
    await db.refresh(course)
    return course

@app.delete('/api/v1/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    
    await db.delete(course)
    await db.commit()
    return None

@app.get('/api/v1/courses/{course_id}/students/', response_model=List[schemas.StudentResponse], tags=['Courses'])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.execute(select(models.Course).filter(models.Course.id == course_id))
    if course.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
        
    query = select(models.Student).join(models.Enrollment).filter(models.Enrollment.course_id == course_id)
    result = await db.execute(query)
    return result.scalars().all()

# --- STUDENTS ---
@app.post('/api/v1/students/', response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(student: schemas.StudentCreate, response: Response, db: AsyncSession = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    response.headers['Location'] = f'/api/v1/students/{db_student.id}/'
    return db_student

@app.get('/api/v1/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} does not exist")
    return student

@app.put('/api/v1/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'])
async def update_student(student_id: int, student_update: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} does not exist")
    
    update_data = student_update.model_dump()
    for key, value in update_data.items():
        setattr(student, key, value)
    
    await db.commit()
    await db.refresh(student)
    return student

@app.patch('/api/v1/students/{student_id}', response_model=schemas.StudentResponse, tags=['Students'])
async def patch_student(student_id: int, student_update: schemas.StudentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} does not exist")
    
    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    await db.commit()
    await db.refresh(student)
    return student

@app.delete('/api/v1/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).filter(models.Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} does not exist")
    
    await db.delete(student)
    await db.commit()
    return None

# --- ENROLLMENTS ---
def send_confirmation_email(student_email: str):
    print(f'Sending confirmation to {student_email}')

@app.post('/api/v1/enrollments/', response_model=schemas.EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
async def create_enrollment(enrollment: schemas.EnrollmentCreate, response: Response, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    response.headers['Location'] = f'/api/v1/enrollments/{db_enrollment.id}/'
    
    student_res = await db.execute(select(models.Student).filter(models.Student.id == enrollment.student_id))
    student = student_res.scalar_one_or_none()
    if student and student.email:
        background_tasks.add_task(send_confirmation_email, student.email)
        
    return db_enrollment

@app.get('/api/v1/enrollments/{enrollment_id}', response_model=schemas.EnrollmentResponse, tags=['Enrollments'])
async def get_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).filter(models.Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail=f"Enrollment with id {enrollment_id} does not exist")
    return enrollment

@app.delete('/api/v1/enrollments/{enrollment_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Enrollments'])
async def delete_enrollment(enrollment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).filter(models.Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    if enrollment is None:
        raise HTTPException(status_code=404, detail=f"Enrollment with id {enrollment_id} does not exist")
    
    await db.delete(enrollment)
    await db.commit()
    return None
