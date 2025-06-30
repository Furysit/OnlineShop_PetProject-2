
import pytest
from contextlib import nullcontext as does_not_raise


@pytest.mark.asyncio
async def test_register_user(client, created_user):
    response = await client.post("/api/v1/users/users/create",
                                 json={
                                     "username" : "testuser",
                                     "email": "test@mail.com",
                                     "password":"password"
                                 })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"

@pytest.mark.asyncio
async def test_get_user(client):
    response = await client.get(
        "/api/v1/users/users/get_users")
    assert response.status_code == 200
    print(response.json())
    
@pytest.mark.asyncio
async def test_login_and_get_token(client):
    await client.post("/api/v1/users/users/create", json={
        "username": "user1",
        "email": "user1@mail.com",
        "password": "password"
    })

    response = await client.post("/api/v1/login", data={
        "username": "user1@mail.com",
        "password": "password"
    })

    assert response.status_code == 200
    


@pytest.mark.parametrize(
        "user_id, expected_status",
        [
            (1, 200),
            ("two", 422),
            (124, 404)
        ]
)
@pytest.mark.asyncio
async def test_get_user_by_id(client, user_id, expected_status):

    await client.post("/api/v1/users/users/create", json={
        "username": "user1",
        "email": "user1@mail.com",
        "password": "password"
    })
    
    response = await client.get(f"/api/v1/users/users/{user_id}")
    
    assert response.status_code == expected_status


@pytest.mark.parametrize(
        "user_id, expected_status",
        [
            (1,204),
            (2,204)
        ]
)
@pytest.mark.asyncio
async def test_delete_user(client, user_id, expected_status):
    response = await client.delete(f"/api/v1/users/users/delete/{user_id}")

    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_get_current_user(client, auth_headers):
    response = await client.get("/api/v1/users/users/me", headers=auth_headers)

    assert response.status_code == 200
    assert "is authorized" in response.json() 

@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client):
    response = await client.get("/api/v1/users/users/me")  
    assert response.status_code == 401
