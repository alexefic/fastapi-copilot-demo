from fastapi import APIRouter
from .books import router as books_router
from .cart import router as cart_router

router = APIRouter()
router.include_router(books_router, prefix='/books', tags=['books'])
router.include_router(cart_router, prefix='/cart', tags=['cart'])
