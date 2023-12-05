from fastapi import APIRouter

from backend.app.api.deps import UserDep
from backend.app.controllers.user_plan_controller import UserPlanController
from backend.app.schemas.plan import Plan
from backend.app.schemas.save_exercises import SaveExercisesModel

router = APIRouter()


@router.post('/add-plan')
async def add_user_exercise(plan: Plan, user: UserDep):
    return UserPlanController().add_plan(plan, user)

@router.get('/get-plans/{page}')
async def get_plans(user: UserDep, page: int):
    return UserPlanController().get_plan_page(user.email, page)

@router.post('/save-exercises')
async def save_exercises(user: UserDep, save_exercises_model: SaveExercisesModel):
    return UserPlanController().save_exercises(
        user.email,
        save_exercises_model.plan_id,
        save_exercises_model.exercise_id_list
    )
@router.get('/get-exercises/{plan_id}')
async def get_exercises(user: UserDep, plan_id: str):
    return UserPlanController().get_exercises(user.email, plan_id)

@router.get('/get-exercises-id/{plan_id}')
async def get_exercises_id(user: UserDep, plan_id: str):
    return UserPlanController().get_exercises_id(user.email, plan_id)
