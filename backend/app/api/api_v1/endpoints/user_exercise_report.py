from fastapi import APIRouter
from backend.app.api.deps import UserDep
from backend.app.controllers.user_exercise_report_controller import UserExerciseReportController
from backend.app.schemas.lift_exercise_report import LiftExerciseReport

router = APIRouter()


@router.post('/add-lift-report')
async def sign_up_endpoint(lift_exercise_report: LiftExerciseReport, user: UserDep):
    return UserExerciseReportController().add_lift_exercise_report(lift_exercise_report, user.email)
