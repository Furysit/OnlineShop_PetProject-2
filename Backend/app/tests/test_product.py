import pytest

@pytest.mark.asyncio
async def test_add_product(client):
    response = await client.post(
        "/api/v1/products/",
        json ={
            "name": "test_name",
            "description": "test_description",
            "price": 10000,
            "category_id": 1
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["price"] == 10000

@pytest.mark.asyncio
async def test_get_all_products(client):
    response = await client.get("/api/v1/products/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_product_by_id(client):
    
    response = await client.get("/api/v1/products/1")
    assert response.status_code == 200


