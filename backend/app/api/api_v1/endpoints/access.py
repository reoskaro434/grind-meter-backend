from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.app.api.deps import UserDep
from backend.app.controllers.access_controller import AccessController

router = APIRouter()


class NewUser(BaseModel):
    newUser: dict


@router.post('/sign-up')
async def sign_up_endpoint(new_user: NewUser):
    return AccessController().create_account(new_user.newUser)


class User(BaseModel):
    user: dict


@router.post("/sign-in")
async def sign_in_endpoint(user: User):
    return AccessController().sign_in(user.user)


@router.get("/refresh-token")
async def refresh_token_endpoint(request: Request):
    ref_token = request.cookies.get("refreshToken")
    username = request.headers.get("username")
    return AccessController().refresh_token(ref_token, username)


class VerifyAccount(BaseModel):
    username: str
    confirmationCode: str


@router.post('/verify-account')
async def verify_account_endpoint(verify_account: VerifyAccount):
    return AccessController().verify_account(verify_account.username, verify_account.confirmationCode)


@router.post('/sign-out')
async def sign_out_endpoint(user: UserDep):
    return AccessController().sign_out(user.access_token)
