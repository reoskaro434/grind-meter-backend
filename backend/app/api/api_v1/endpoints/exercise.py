from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.app.api.deps import UserDep
from backend.app.controllers.access_controller import AccessController

router = APIRouter()


@router.post('/lift')
async def sign_up_endpoint(lift_exercise_report: NewUser):
    return AccessController().create_account(new_user.newUser)
