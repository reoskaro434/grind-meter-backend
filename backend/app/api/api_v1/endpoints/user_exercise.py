from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.api.deps import UserDep
from backend.app.controllers.user_exercise_controller import UserExerciseController
from backend.app.schemas.exercise import Exercise
from backend.app.schemas.exercise_id import ExerciseId

router = APIRouter()


@router.post('/add-exercise')
async def add_user_exercise(exercise: Exercise, user: UserDep):
    return UserExerciseController().add_exercise(exercise, user)


@router.get('/get-exercises/{page}')
async def get_exercises(user: UserDep, page: int):
    return UserExerciseController().get_exercise_page(user.email, page)

@router.post('/set-active')
async def set_exercise_active(exercise_id: ExerciseId, user: UserDep):
    return UserExerciseController().set_exercise_active(exercise_id, user)


@router.post('/set-inactive')
async def set_exercise_inactive(exercise_id: ExerciseId, user: UserDep):
    return UserExerciseController().set_exercise_inactive(exercise_id, user)

@router.get('/get-active-exercises')
async def get_active_exercises(user: UserDep):
    return UserExerciseController().get_active_exercises(user.email, 1)