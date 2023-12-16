from fastapi import APIRouter

from backend.app.api.deps import UserDep
from backend.app.controllers.user_plan_controller import UserPlanController
from backend.app.schemas.plan import Plan

router = APIRouter()


@router.post('/add-plan')
async def add_user_exercise(plan: Plan, user: UserDep):
    return UserPlanController().add_plan(plan, user)

@router.get('/get-plan/{plan_id}')
async def get_plan(user: UserDep, plan_id: str):
    return UserPlanController().get_plan(user.email, plan_id)

@router.post('/update')
async def update(plan: Plan, user: UserDep):
    return UserPlanController().update(plan, user.email)

@router.delete('/delete/{plan_id}')
async def delete(plan_id: str, user: UserDep):
    return UserPlanController().delete(plan_id, user.email)

@router.get('/get-plans')
async def get_plans(user: UserDep):
    return UserPlanController().get_plans_for_account(user.email)

@router.get('/get-exercises/{plan_id}')
async def get_exercises(user: UserDep, plan_id: str):
    return UserPlanController().get_exercises(user.email, plan_id)
