from fastapi import APIRouter

from .users.views import router as users_router
from .products.views import router as products_router
from .users.auth import router as auth_router
from .cart.views import router as cart_router
from .orders.views import router as orders_router
from .admin.views import router as admin_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=products_router, prefix="/products")
router.include_router(router=cart_router, prefix="/cart")
router.include_router(router=orders_router, prefix="/orders")
router.include_router(router=admin_router, prefix="/admin")
router.include_router(router=auth_router)