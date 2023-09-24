from fastapi import APIRouter, Request, Header
from pydantic import BaseModel

from backend.controllers.access_controller import AccessController
# from backend.decorators import require_authentication

ACCESS_ROUTER = APIRouter()


class NewUser(BaseModel):
    newUser: dict


@ACCESS_ROUTER.post('/access/sign-up')
def sign_up_endpoint(new_user: NewUser):
    print('hello')
    return AccessController().create_account(new_user.newUser)


class User(BaseModel):
    user: dict


@ACCESS_ROUTER.post("/access/sign-in")
def sign_in_endpoint(user: User):
    return AccessController().sign_in(user.user)


@ACCESS_ROUTER.get("/access/refresh-token")
def refresh_token_endpoint(request: Request):
    ref_token = request.cookies.get("refreshToken")
    username = request.headers.get("username")
    return AccessController().refresh_token(ref_token, username)


class VerifyAccount(BaseModel):
    username: str
    confirmationCode: str


@ACCESS_ROUTER.post('/access/verify-account')
def verify_account_endpoint(verify_account: VerifyAccount):
    return AccessController().verify_account(verify_account.username, verify_account.confirmationCode)


@ACCESS_ROUTER.post('/access/sign-out')
# @require_authentication
def sign_out_endpoint(access_token: str = Header(None)):
    return AccessController().sign_out(access_token)
