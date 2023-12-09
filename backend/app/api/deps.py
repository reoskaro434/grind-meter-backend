from fastapi import HTTPException, Request, Depends
from typing import Annotated

from backend.app.aws.cognito_provider import CognitoProvider
from backend.app.aws.secret_provider import SecretProvider
from backend.app.global_settings import global_settings as g
from backend.app.schemas.user import UserAuthorized

def __raise_exception():
    raise HTTPException(status_code=401, detail="Cannot get current user")
async def get_current_user(request: Request):
    access_token = request.cookies.get("accessToken")

    if not access_token:
        __raise_exception()

    cognito_pool_data = SecretProvider(
        g.REGION,
        g.POOL_CLIENT_DATA_SECRET_NAME
    ).get_secret()

    cognito_provider = CognitoProvider(
        cognito_pool_data.get("COGNITO_POOL_CLIENT_ID"),
        cognito_pool_data.get("COGNITO_POOL_CLIENT_SECRET"))

    user = cognito_provider.get_user(access_token)
    if not user:
        __raise_exception()

    # Get email from array of obj
    email_obj = [obj for obj in user.get("UserAttributes") if obj.get("Name") == "email"]

    user_authorized = UserAuthorized(
        access_token=access_token,
        username=user.get("Username"),
        email=email_obj.pop().get("Value")
    )

    return user_authorized


UserDep = Annotated[UserAuthorized, Depends(get_current_user)]
