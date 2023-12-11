from fastapi import APIRouter

from backend.app.api.deps import UserDep
from backend.app.controllers.user_exercise_controller import UserExerciseController
from backend.app.schemas.exercise import Exercise

router = APIRouter()


@router.post('/add-exercise')
async def add_user_exercise(exercise: Exercise, user: UserDep):
    return UserExerciseController().add_exercise(exercise, user)

@router.get('/get-exercises')
async def get_exercises(user: UserDep):
    return UserExerciseController().get_exercise_page(user.email)

@router.get('/get-exercise/{exercise_id}')
async def get_exercise(user: UserDep, exercise_id: str):
    return UserExerciseController().get_exercise(user.email, exercise_id)

@router.post('/update')
async def update(exercise: Exercise, user: UserDep):
    return UserExerciseController().rename(exercise.id, user.email, exercise.name)
