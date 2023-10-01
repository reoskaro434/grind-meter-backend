from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.app.api.deps import UserDep
from backend.app.controllers.access_controller import AccessController
from backend.app.schemas.lift_exercise_report import LiftExerciseReport

router = APIRouter()

#
# @router.post('/lift-report')
# async def sign_up_endpoint(lift_exercise_report: LiftExerciseReport):
#     return AccessController().create_account(new_user.newUser)
