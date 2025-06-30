
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.app import app
from app.core.models import Base, db_helper

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(DATABASE_URL_TEST, echo=True)
SessionTest = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()

@pytest_asyncio.fixture
async def session():
    async with SessionTest() as s:
        yield s

@pytest_asyncio.fixture
async def client(session: AsyncSession):
    
    async def override_scoped_session():
        yield session

    app.dependency_overrides[db_helper.scoprd_session_dependecy] = override_scoped_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest_asyncio.fixture
async def created_user(client):
    await client.post("/api/v1/users/users/create",
                                 json={
                                     "username" : "ABA",
                                     "email": "test_ABA@mail.com",
                                     "password":"password"
                                 })
    
@pytest_asyncio.fixture
async def created_product(client):
    await client.post(
        "/api/v1/products/",
        json ={
            "name": "test_name",
            "description": "test_description",
            "price": 10000,
            "category_id": 1
        }
    )


import pytest_asyncio

@pytest_asyncio.fixture
async def auth_headers(client):
    # Создаём пользователя
    await client.post("/api/v1/users/users/create", json={
        "username": "authuser",
        "email": "auth@mail.com",
        "password": "password"
    })

    response = await client.post("/api/v1/login", data={
        "username": "auth@mail.com",
        "password": "password"
    })

    print("Login response:", response.status_code, response.text)

    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}