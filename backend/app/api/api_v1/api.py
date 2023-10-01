from fastapi import APIRouter

from backend.app.api.api_v1.endpoints import access, user_exercise, user_exercise_report

api_router = APIRouter()

api_router.include_router(access.router, prefix="/access", tags=["access"])
api_router.include_router(user_exercise_report.router, prefix="/user-exercise-report", tags=["user exercise report"])
api_router.include_router(user_exercise.router, prefix="/user-exercise", tags=["user exercise"])
