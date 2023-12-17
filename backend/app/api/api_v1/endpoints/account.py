from fastapi import APIRouter

from backend.app.api.deps import UserDep
from backend.app.controllers.account_controller import AccountController
from backend.app.schemas.account import Account

router = APIRouter()

@router.post('/update')
async def update(account: Account, user: UserDep):
    return AccountController().update(account, user.email)

@router.get('/get')
async def get(user: UserDep):
    return AccountController().get_account(user.email)
