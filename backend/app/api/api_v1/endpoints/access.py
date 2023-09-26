from fastapi import APIRouter, Request, Header
from pydantic import BaseModel

from backend.app.controllers.access_controller import AccessController
# from backend.app.decorators import require_authentication

router = APIRouter()


class NewUser(BaseModel):
    newUser: dict


@router.post('/sign-up')
def sign_up_endpoint(new_user: NewUser):
    return AccessController().create_account(new_user.newUser)


class User(BaseModel):
    user: dict


@router.post("/sign-in")
def sign_in_endpoint(user: User):
    return AccessController().sign_in(user.user)


@router.get("/refresh-token")
def refresh_token_endpoint(request: Request):
    ref_token = request.cookies.get("refreshToken")
    username = request.headers.get("username")
    return AccessController().refresh_token(ref_token, username)


class VerifyAccount(BaseModel):
    username: str
    confirmationCode: str


@router.post('/verify-account')
def verify_account_endpoint(verify_account: VerifyAccount):
    return AccessController().verify_account(verify_account.username, verify_account.confirmationCode)


@router.post('/sign-out')
# @require_authentication
def sign_out_endpoint(access_token: str = Header(None)):
    return AccessController().sign_out(access_token)
