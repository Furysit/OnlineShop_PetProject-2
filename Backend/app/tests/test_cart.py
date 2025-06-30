import pytest

@pytest.mark.asyncio
async def test_add_product_to_cart(client, created_user, created_product):
    response = await client.post(
        "/api/v1/cart/add_product?user_id=1",
        json={
            "product_id" : 1,
            "quantity": 1
        }
    )
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_cart(client,created_user):
    response = await client.get(
        "/api/v1/cart/get_cart?user_id=1"
    )
    assert response.status_code == 200