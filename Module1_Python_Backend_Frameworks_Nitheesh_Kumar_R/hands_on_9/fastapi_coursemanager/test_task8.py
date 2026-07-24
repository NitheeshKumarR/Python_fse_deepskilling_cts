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
        
        # Test 201 Location header
        response = await ac.post("/api/v1/courses/", json={
            "name": "Advanced Python", "code": "CS401", "credits": 4, "department_id": 1
        })
        assert response.status_code == 201
        assert "Location" in response.headers
        assert response.headers["Location"] == "/api/v1/courses/1/"
        
        # Test offset pagination & search
        response = await ac.get("/api/v1/courses/?page=1&page_size=10&search=python")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "next" in data
        assert "previous" in data
        assert "results" in data
        assert data["count"] == 1
        assert data["results"][0]["code"] == "CS401"
        
        # Test custom 404 handler format
        response = await ac.get("/api/v1/courses/99")
        assert response.status_code == 404
        error_data = response.json()
        assert "error" in error_data
        assert error_data["error"]["code"] == "NOT_FOUND"
        assert "99" in error_data["error"]["message"]

        # Test custom validation 422 handler format
        response = await ac.post("/api/v1/courses/", json={"bad": "data"})
        assert response.status_code == 422
        error_data = response.json()
        assert error_data["error"]["code"] == "UNPROCESSABLE_ENTITY"
        assert error_data["error"]["field"] is not None

        # Test PATCH
        response = await ac.patch("/api/v1/courses/1", json={"credits": 5})
        assert response.status_code == 200
        assert response.json()["credits"] == 5

        print("All API routes worked properly with REST best practices!")

if __name__ == "__main__":
    asyncio.run(test_api())
