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
            from sqlalchemy import insert
            await conn.execute(insert(models.Department).values(name="CS"))
        
        # Test Registration
        response = await ac.post("/api/v1/auth/register/", json={
            "email": "test@test.com", "password": "mypassword"
        })
        assert response.status_code == 201

        # Test Registration Conflict
        response = await ac.post("/api/v1/auth/register/", json={
            "email": "test@test.com", "password": "mypassword2"
        })
        assert response.status_code == 409

        # Test Login
        response = await ac.post("/api/v1/auth/login/", data={
            "username": "test@test.com", "password": "mypassword"
        })
        assert response.status_code == 200
        token = response.json()["access_token"]
        assert token is not None

        # Test Unauthenticated access to protected route
        response = await ac.post("/api/v1/courses/", json={
            "name": "Secure Course", "code": "SEC101", "credits": 3, "department_id": 1
        })
        assert response.status_code == 401

        # Test Authenticated access to protected route
        response = await ac.post("/api/v1/courses/", json={
            "name": "Secure Course", "code": "SEC101", "credits": 3, "department_id": 1
        }, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 201

        print("All authentication tests passed successfully!")

if __name__ == "__main__":
    asyncio.run(test_api())
