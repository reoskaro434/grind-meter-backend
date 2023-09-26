import base64
import os
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from backend.app.aws.cognito_provider import CognitoProvider
from backend.app.aws.secret_provider import SecretProvider
from backend.app.globals import REFRESH_TOKEN_EXPIRE
from datetime import datetime


class AccessController:
    def __init__(self):
        region = os.environ.get("REGION", "eu-central-1")
        stage = os.environ.get("STAGE", "dev")
        self._cognito_pool_data = SecretProvider(
            region,
            f"GRIND_METER_COGNITO_POOL_CLIENT_DATA_{stage.upper()}_{region.upper()}"
        ).get_secret()
        self._cognito_provider = CognitoProvider(
            self._cognito_pool_data.get("COGNITO_POOL_CLIENT_ID"),
            self._cognito_pool_data.get("COGNITO_POOL_CLIENT_SECRET"))

    def sign_in(self, user):
        cognito_result = self._cognito_provider.sign_in(user)
        if cognito_result is not False:
            payload = {
                "accessToken": cognito_result["AuthenticationResult"]["AccessToken"],
            }
            response = JSONResponse(content={"payload": payload})
            response.set_cookie(key="refreshToken",
                                value=cognito_result["AuthenticationResult"]["RefreshToken"],
                                samesite="none",
                                secure=True,
                                httponly=True,
                                expires=datetime.now().timestamp() + REFRESH_TOKEN_EXPIRE * 60)
            response.set_cookie(key="username",
                                value=base64.b64encode(user.get("username").encode()).decode(),
                                samesite="none",
                                secure=True,
                                domain="grind-meter.com",
                                expires=datetime.now().timestamp() + REFRESH_TOKEN_EXPIRE * 60)
            return response
        raise HTTPException(status_code=401)

    def refresh_token(self, refresh_token, username):
        response = self._cognito_provider.refresh_token(refresh_token, username)
        if response is not False:
            payload = {
                "accessToken": response["AuthenticationResult"]["AccessToken"]
            }
            return {"payload": payload}

        raise HTTPException(status_code=401)

    def create_account(self, new_user):
        result = self._cognito_provider.create_user(new_user)
        if result is True:
            return {"success": result}

        raise HTTPException(status_code=400)

    def verify_account(self, username, confirmation_code):
        result = self._cognito_provider.verify_account(username, confirmation_code)
        if result is True:
            return {"success": result}

        raise HTTPException(status_code=400)

    def sign_out(self, access_token):
        result = self._cognito_provider.sign_out(access_token)

        if result is True:
            return {"success": result}

        raise HTTPException(status_code=500)
