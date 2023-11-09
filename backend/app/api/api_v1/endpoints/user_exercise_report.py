from fastapi import APIRouter
from backend.app.api.deps import UserDep
from backend.app.schemas.lift_exercise_report import LiftExerciseReport

router = APIRouter()


@router.post('/add-lift-report')
async def sign_up_endpoint(lift_exercise_report: LiftExerciseReport, user: UserDep):
    print('hello')
    print(lift_exercise_report)
    print(user)
    return True
