from fastapi import APIRouter

from backend.app.api.api_v1.endpoints import access, exercise, exercise_report, plan

api_router = APIRouter()

api_router.include_router(access.router, prefix="/access", tags=["access"])
api_router.include_router(exercise_report.router, prefix="/exercise-report", tags=["exercise report"])
api_router.include_router(exercise.router, prefix="/exercise", tags=["exercise"])
api_router.include_router(plan.router, prefix="/plan", tags=["plan"])
