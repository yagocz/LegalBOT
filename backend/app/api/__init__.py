from fastapi import APIRouter
from app.api.users import router as users_router
from app.api.chat import router as chat_router
from app.api.documents import router as documents_router

api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(chat_router)
api_router.include_router(documents_router)

