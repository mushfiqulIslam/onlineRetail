from fastapi import APIRouter

from api.v1.api import bot_router

v1_router = APIRouter()
v1_router.include_router(bot_router, prefix="/chat", tags=["chat"])