from typing import List

from fastapi import APIRouter

from backend.app.api.deps import UserDep
from backend.app.controllers.user_exercise_controller import UserExerciseController
from backend.app.controllers.user_plan_controller import UserPlanController
from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_id import ExerciseId
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
async def saveExercises(user: UserDep, saveExercisesModel: SaveExercisesModel):
    return UserPlanController().save_exercises(user.email, saveExercisesModel.plan_id, saveExercisesModel.exercise_id_list)
#
# @router.get('/get-plan/{plan_id}')
# async def get_plan(user: UserDep, exercise_id: str):
#     return UserExerciseController().get_exercise(user.email, exercise_id)
#
# @router.post('/set-active')
# async def set_exercise_active(exercise_id: ExerciseId, user: UserDep):
#     return UserExerciseController().set_exercise_active(exercise_id, user)
#
# @router.post('/set-inactive')
# async def set_exercise_inactive(exercise_id: ExerciseId, user: UserDep):
#     return UserExerciseController().set_exercise_inactive(exercise_id, user)
#
# @router.get('/get-active-plan')
# async def get_active_plan(user: UserDep):
#     return UserExerciseController().get_active_exercises(user.email, 1)