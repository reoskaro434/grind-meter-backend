from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.app.api.deps import UserDep
from backend.app.controllers.access_controller import AccessController
from backend.app.controllers.user_exercise_controller import UserExerciseController
from backend.app.schemas.exercise import Exercise

router = APIRouter()


@router.post('/add-exercise')
async def add_user_exercise(exercise: Exercise, user: UserDep):
    return UserExerciseController().add_exercise(exercise, user)


@router.get('/get-exercise/{page}')
async def add_user_exercise(user: UserDep, page: int):
    return UserExerciseController().get_exercise_page(user.email, page)
