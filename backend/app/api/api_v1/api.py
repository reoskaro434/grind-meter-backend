from fastapi import APIRouter

from backend.app.api.api_v1.endpoints import access

api_router = APIRouter()

api_router.include_router(access.router, prefix="/access", tags=["access"])
