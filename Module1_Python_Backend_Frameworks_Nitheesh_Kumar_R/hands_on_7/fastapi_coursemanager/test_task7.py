import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app, engine, Base
import models

@pytest.mark.asyncio
async def test_api():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create department
        async with engine.begin() as conn:
            # We don't have department routes so inject one manually for foreign key constraints
            from sqlalchemy import insert
            await conn.execute(insert(models.Department).values(name="CS"))
        
        # Create Course
        response = await ac.post("/api/courses/", json={
            "name": "Math 101", "code": "M101", "credits": 3, "department_id": 1
        })
        assert response.status_code == 201
        
        # Create Student
        response = await ac.post("/api/students/", json={
            "first_name": "John", "last_name": "Doe", "email": "john@test.com", 
            "enrollment_year": 2024, "department_id": 1
        })
        assert response.status_code == 201

        # Create Enrollment (should trigger background task)
        response = await ac.post("/api/enrollments/", json={
            "student_id": 1, "course_id": 1, "grade": "A"
        })
        assert response.status_code == 201
        
        # Get course students
        response = await ac.get("/api/courses/1/students/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["email"] == "john@test.com"

        print("All API routes worked properly!")

if __name__ == "__main__":
    asyncio.run(test_api())
